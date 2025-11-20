"""
CLI Commands

Click-based CLI for blog-agent.
"""
import click
from pathlib import Path
import sys
from builtins import list as list_type

from ...core.domain.article import Article
from ...core.domain.config import ArticleConfig
from ...core.workflow.engine import WorkflowEngine
from ...core.factory import DependencyFactory


@click.group(context_settings={'help_option_names': ['-h', '--help']})
@click.version_option(version='1.0.0')
def cli():
    """
    Blog Agent - AI-powered article generation system

    Automatically generates blog articles with AI review and git versioning.
    """
    pass


@cli.command()
@click.option('--series', required=True, help='Series name (e.g., ecommerce, strony-internetowe)')
@click.option('--silo', help='Silo name (e.g., operacje, platformy) - optional when initializing entire series')
@click.option('--slug', help='Article slug (e.g., bezpieczenstwo-rodo) - required for single article')
@click.option('--title', help='Article title (H1) - required for single article')
@click.option('--audience', help='Target audience - required for single article')
@click.option('--tone', default='ekspercki, ale naturalny i rozmowny', help='Writing tone')
def init(series: str, silo: str, slug: str, title: str, audience: str, tone: str):
    """
    Initialize article structure

    Two modes:
    1. Initialize entire series: blog-agent init --series strony-internetowe
       (reads article_structure.yaml and creates all silos/articles)

    2. Initialize single article: blog-agent init --series ecommerce --silo operacje --slug bezpieczenstwo-rodo --title "..." --audience "..."

    Examples:
        # Initialize entire series from article_structure.yaml
        blog-agent init --series strony-internetowe

        # Initialize single article
        blog-agent init --series ecommerce --silo operacje --slug bezpieczenstwo-rodo --title "Bezpieczeństwo i RODO" --audience "Właściciele sklepów e-commerce"
    """
    import yaml

    project_root = Path.cwd()

    # MODE 1: Initialize entire series from article_structure.yaml
    if not silo and not slug:
        click.echo(f"🚀 Initializing series: {series}")
        click.echo(f"   Reading article_structure.yaml...\n")

        # Read article_structure.yaml
        yaml_file = project_root / "article_structure.yaml"
        if not yaml_file.exists():
            click.echo(f"❌ article_structure.yaml not found")
            sys.exit(1)

        with open(yaml_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        structure = data.get('structure', {})

        if series not in structure:
            click.echo(f"❌ Series '{series}' not found in article_structure.yaml")
            click.echo(f"\n   Available series: {', '.join(structure.keys())}")
            sys.exit(1)

        series_data = structure[series]

        # Initialize factory once
        factory = DependencyFactory(project_root)
        deps = factory.create_deps()

        # Stats
        created_count = 0
        skipped_count = 0

        # Process each silo
        for silo_name, articles in series_data.items():
            if not isinstance(articles, list_type):
                click.echo(f"⚠️  Skipping {silo_name} - invalid format")
                continue

            click.echo(f"\n📁 Silo: {silo_name}")

            # 1. Create article for the silo itself (silos are always articles)
            silo_path = project_root / "artykuly" / series / silo_name

            if silo_path.exists() and (silo_path / "config.yaml").exists():
                click.echo(f"  📄 [silo article] (already exists)")
                skipped_count += 1
            else:
                # Convert slug to title
                silo_title = silo_name.replace('-', ' ').title()

                silo_config = ArticleConfig(
                    title=silo_title,
                    target_audience=audience or "Przedsiębiorcy i właściciele firm",
                    tone=tone
                )

                # Create silo article
                silo_article = Article(path=silo_path, config=silo_config)

                # Execute init step for silo
                from ...core.workflow.steps.step_01_init import execute_init
                execute_init(silo_article, deps, {})

                click.echo(f"  ✅ [silo article] {silo_name}")
                created_count += 1

            # 2. Process each article in the silo
            for article_slug in articles:
                article_path = project_root / "artykuly" / series / silo_name / article_slug

                # Skip if exists
                if article_path.exists():
                    click.echo(f"  ⏭️  {article_slug} (already exists)")
                    skipped_count += 1
                    continue

                # Create default config
                # Convert slug to title (replace - with spaces, capitalize)
                article_title = article_slug.replace('-', ' ').title()

                config = ArticleConfig(
                    title=article_title,
                    target_audience=audience or "Przedsiębiorcy i właściciele firm",
                    tone=tone
                )

                # Create article
                article = Article(path=article_path, config=config)

                # Execute init step
                from ...core.workflow.steps.step_01_init import execute_init
                execute_init(article, deps, {})

                click.echo(f"  ✅ {article_slug}")
                created_count += 1

        click.echo(f"\n{'='*60}")
        click.echo(f"📊 Summary:")
        click.echo(f"   Created: {created_count}")
        click.echo(f"   Skipped: {skipped_count}")
        click.echo(f"{'='*60}")

        return

    # MODE 2: Initialize single article (original behavior)
    if not slug or not title or not audience:
        click.echo("❌ For single article initialization, all parameters are required:")
        click.echo("   --series, --silo, --slug, --title, --audience")
        click.echo("\nOr use series-only mode to initialize entire series:")
        click.echo("   blog-agent init --series strony-internetowe")
        sys.exit(1)

    # Build article path
    article_path = project_root / "artykuly" / series / silo / slug

    # Check if already exists
    if article_path.exists():
        click.echo(f"❌ Article already exists: {article_path}")
        sys.exit(1)

    # Create config
    config = ArticleConfig(
        title=title,
        target_audience=audience,
        tone=tone
    )

    # Create article
    article = Article(path=article_path, config=config)

    # Create factory
    factory = DependencyFactory(project_root)
    deps = factory.create_deps()

    # Execute init step
    from ...core.workflow.steps.step_01_init import execute_init
    execute_init(article, deps, {})

    click.echo(f"✅ Article initialized: {article_path}")
    click.echo(f"\nNext step:")
    click.echo(f"  blog-agent create --config {article_path}/config.yaml")


@cli.command()
@click.option('--config', 'config_path', required=True, type=click.Path(exists=True), help='Path to config.yaml')
@click.option('--provider', default='claude', help='AI provider (default: claude)')
@click.option('--skip', help='Steps/groups to skip (comma-separated). Steps: init,outline,summary,write_sections,create_draft,seo_review,humanize,multimedia,business_metadata,cta,publish,schema,categories,internal_linking. Groups: writing,post-processing,metadata,all-except-outline')
@click.option('--only', help='Only run these steps (comma-separated, e.g., outline,summary)')
def create(config_path: str, provider: str, skip: str, only: str):
    """
    Generate complete article

    Runs full workflow from outline to publication.

    Step Groups (for --skip):
      - writing: outline,summary,write_sections,create_draft
      - post-processing: seo_review,humanize
      - metadata: multimedia,business_metadata,schema,categories,internal_linking
      - all-except-outline: All steps except outline (keeps existing outline.md)

    Examples:
      # Full workflow
      blog-agent create --config artykuly/ecommerce/seo/config.yaml

      # Skip outline (use existing outline.md)
      blog-agent create --config artykuly/ecommerce/seo/config.yaml --skip outline

      # Skip all writing steps (use existing content)
      blog-agent create --config artykuly/ecommerce/seo/config.yaml --skip writing

      # Skip outline and all metadata steps
      blog-agent create --config artykuly/ecommerce/seo/config.yaml --skip outline,metadata

      # Only generate outline
      blog-agent create --config artykuly/ecommerce/seo/config.yaml --only outline

      # Only write sections (requires existing outline)
      blog-agent create --config artykuly/ecommerce/seo/config.yaml --only write_sections
    """
    config_path = Path(config_path)
    project_root = Path.cwd()

    # Load article config
    article_config = ArticleConfig.from_yaml(config_path)

    # Get article path (parent of config.yaml)
    article_path = config_path.parent

    # Create article
    article = Article(path=article_path, config=article_config)

    click.echo(f"🚀 Generating article: {article.config.title}")
    click.echo(f"   Path: {article_path}")
    click.echo(f"   Provider: {provider}\n")

    # Define step groups for easier skipping
    STEP_GROUPS = {
        'writing': ['outline', 'summary', 'write_sections', 'create_draft'],
        'post-processing': ['seo_review', 'humanize'],
        'metadata': ['multimedia', 'business_metadata', 'schema', 'categories', 'internal_linking'],
        'all-except-outline': ['init', 'summary', 'write_sections', 'create_draft', 'seo_review',
                               'humanize', 'multimedia', 'business_metadata', 'cta', 'publish',
                               'schema', 'categories', 'internal_linking', 'generate_images'],
    }

    def expand_groups(items_str: str) -> list:
        """Expand step groups into individual steps"""
        if not items_str:
            return None

        items = [s.strip() for s in items_str.split(',')]
        expanded = []

        for item in items:
            if item in STEP_GROUPS:
                # It's a group - expand it
                expanded.extend(STEP_GROUPS[item])
            else:
                # It's a regular step name
                expanded.append(item)

        # Remove duplicates while preserving order
        seen = set()
        result = []
        for step in expanded:
            if step not in seen:
                seen.add(step)
                result.append(step)

        return result if result else None

    # Parse skip/only lists (with group expansion)
    skip_list = expand_groups(skip)
    only_list = expand_groups(only)

    # Auto-detect provider from model name if provider is default 'claude'
    # and article config has a specific model
    detected_provider = provider
    if provider == 'claude' and article_config.model:
        model = article_config.model
        # Map common model patterns to providers
        if model.startswith('gpt-') or 'gpt' in model.lower():
            # Try to find matching provider config (e.g., openai-gpt5-1 for gpt-5.1)
            # Normalize: gpt-5.1 -> gpt5-1, gpt-4o -> gpt4o
            model_normalized = model.replace('.', '-').replace('gpt-', 'gpt')
            detected_provider = f'openai-{model_normalized}'
            click.echo(f"   Auto-detected provider: {detected_provider} (from model: {model})")
        elif model.startswith('gemini'):
            detected_provider = 'gemini'
            click.echo(f"   Auto-detected provider: {detected_provider} (from model: {model})")
        elif model.startswith('claude'):
            detected_provider = 'claude'

    # Create factory and deps
    factory = DependencyFactory(project_root)
    deps = factory.create_deps(detected_provider)

    # Create workflow engine (pass factory for per-step provider support)
    workflow_config_path = factory.get_workflow_config_path()
    engine = WorkflowEngine(workflow_config_path, factory=factory)

    # Execute workflow
    try:
        article = engine.execute_workflow(
            article,
            deps,
            skip_steps=skip_list,
            only_steps=only_list
        )

        click.echo(f"\n✅ Article generated successfully!")
        click.echo(f"   Status: {article.status}")
        click.echo(f"   Sections: {len(article.sections)}")
        click.echo(f"   Categories: {len(article.categories)}")
        click.echo(f"\n📄 Final article: {article.get_article_path()}")

    except Exception as e:
        click.echo(f"\n❌ Article generation failed: {str(e)}")
        sys.exit(1)


@cli.command()
@click.option('--config', 'config_path', required=True, type=click.Path(exists=True), help='Path to config.yaml')
@click.option('--provider', default='stability', help='Image provider (stability or dalle)')
@click.option('--size', default='1920x1200', help='Output size (default: 1920x1200 for hero)')
@click.option('--skip-existing', is_flag=True, default=True, help='Skip if hero already exists')
def generate_hero(config_path: str, provider: str, size: str, skip_existing: bool):
    """
    Generate hero image for article

    Generates hero image from multimedia.json and upscales to desired size.
    Run this after article is published to add professional hero image.

    Examples:
        # Generate with Stability AI (cheap, fast)
        blog-agent generate-hero --config artykuly/seria/silos/slug/config.yaml

        # Generate with DALL-E (premium quality)
        blog-agent generate-hero --config artykuly/seria/silos/slug/config.yaml --provider dalle

        # Custom size
        blog-agent generate-hero --config artykuly/seria/silos/slug/config.yaml --size 1920x1080
    """
    import os

    # Load .env if exists
    env_file = Path.cwd() / ".env"
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value

    config_path = Path(config_path).resolve()
    project_root = Path.cwd()

    # Parse size
    try:
        width, height = map(int, size.split('x'))
    except:
        click.echo(f"❌ Invalid size format: {size}")
        click.echo(f"   Use format: WIDTHxHEIGHT (e.g., 1920x1200)")
        sys.exit(1)

    # Load article
    article_config = ArticleConfig.from_yaml(config_path)
    article_path = config_path.parent
    article = Article(path=article_path, config=article_config)

    click.echo(f"🎨 Generating hero image")
    click.echo(f"   Article: {article.config.title}")
    click.echo(f"   Provider: {provider}")
    click.echo(f"   Size: {width}x{height}")

    # Check multimedia.json
    multimedia_path = article.get_multimedia_path()
    if not multimedia_path.exists():
        click.echo(f"\n❌ No multimedia.json found")
        click.echo(f"   Run multimedia step first or create multimedia.json manually")
        sys.exit(1)

    # Check if hero already exists
    hero_path = article_path / 'images' / 'hero.png'
    if skip_existing and hero_path.exists():
        click.echo(f"\n✅ Hero image already exists: {hero_path.name}")
        click.echo(f"   Use --no-skip-existing to regenerate")
        return

    # Create factory and deps
    factory = DependencyFactory(project_root)
    deps = factory.create_deps()

    # Determine optimal generation size based on provider
    if provider == 'stability':
        # Generate native size without upscaling to avoid distortion
        gen_width, gen_height = 1024, 1024
        model = 'sdxl'
        # Override target size to native (no upscale)
        width, height = 1024, 1024
        click.echo(f"   ⚠️  Using native 1024x1024 (no upscale to avoid distortion)")
    elif provider == 'dalle':
        # DALL-E can do 1792x1024 natively
        gen_width, gen_height = 1792, 1024
        model = 'dall-e-3'
    else:
        click.echo(f"❌ Unknown provider: {provider}")
        click.echo(f"   Supported: stability, dalle")
        sys.exit(1)

    click.echo(f"\n🔧 Generation settings:")
    click.echo(f"   Native size: {gen_width}x{gen_height}")
    click.echo(f"   Target size: {width}x{height}")
    if gen_width != width or gen_height != height:
        click.echo(f"   Upscale: Yes (AI will upscale after generation)")

    # Execute generate_images step
    from ...core.workflow.steps.step_15_generate_images import execute_generate_images

    step_config = {
        'provider': provider,
        'model': model,
        'skip_existing': False,  # Force generation since user explicitly requested
    }

    # Add provider-specific settings
    if provider == 'stability':
        step_config.update({
            'width': gen_width,
            'height': gen_height,
            'steps': 40,
            'cfg_scale': 7.0
        })
    elif provider == 'dalle':
        step_config.update({
            'size': f'{gen_width}x{gen_height}',
            'quality': 'standard'
        })

    try:
        click.echo()
        article = execute_generate_images(article, deps, step_config)

        # Upscale if needed
        if hero_path.exists() and (gen_width != width or gen_height != height):
            click.echo(f"\n🔄 Upscaling to {width}x{height}...")
            _upscale_hero(hero_path, width, height)

        click.echo(f"\n✅ Hero image generated successfully!")
        try:
            click.echo(f"   Location: {hero_path.relative_to(project_root)}")
        except ValueError:
            click.echo(f"   Location: {hero_path}")

        # Show cost
        if provider == 'stability':
            click.echo(f"   Cost: ~$0.011")
        elif provider == 'dalle':
            click.echo(f"   Cost: ~$0.08")

    except Exception as e:
        click.echo(f"\n❌ Generation failed: {str(e)}")
        sys.exit(1)


def _upscale_hero(image_path: Path, target_width: int, target_height: int):
    """Upscale hero image to target size using high-quality resize"""
    try:
        from PIL import Image

        # Load image
        img = Image.open(image_path)
        original_size = img.size

        # Resize with high-quality Lanczos filter
        img_resized = img.resize((target_width, target_height), Image.Resampling.LANCZOS)

        # Save
        img_resized.save(image_path, 'PNG', optimize=True)

        click.echo(f"   ✅ Upscaled from {original_size[0]}x{original_size[1]} to {target_width}x{target_height}")

    except ImportError:
        click.echo(f"   ⚠️  Pillow not installed - image saved at native size")
        click.echo(f"   Install: pip install Pillow")
    except Exception as e:
        click.echo(f"   ⚠️  Upscaling failed: {str(e)}")


@cli.command()
@click.option('--path', 'article_path', required=True, help='Path to article directory')
def status(article_path: str):
    """
    Show article status

    Displays current state and progress.

    Example:
        blog-agent status --path artykuly/ecommerce/operacje/bezpieczenstwo-rodo/
    """
    article_path = Path(article_path)

    if not article_path.exists():
        click.echo(f"❌ Article directory not found: {article_path}")
        sys.exit(1)

    # Load config
    config_path = article_path / "config.yaml"
    if not config_path.exists():
        click.echo(f"❌ No config.yaml found in {article_path}")
        sys.exit(1)

    article_config = ArticleConfig.from_yaml(config_path)
    article = Article(path=article_path, config=article_config)

    # Check what exists
    has_outline = article.get_outline_path().exists()
    has_sections = len([p for p in article.get_sections_dir().glob("*.md")]) > 0
    has_draft = article.get_draft_path().exists()
    has_article = article.get_article_path().exists()
    has_categories = article.get_categories_path().exists()

    # Display status
    click.echo(f"\n📊 Article Status: {article.config.title}")
    click.echo(f"   Path: {article_path}\n")

    click.echo("Progress:")
    click.echo(f"  {'✅' if has_outline else '❌'} Outline")
    click.echo(f"  {'✅' if has_sections else '❌'} Sections")
    click.echo(f"  {'✅' if has_draft else '❌'} Draft")
    click.echo(f"  {'✅' if has_article else '❌'} Final Article")
    click.echo(f"  {'✅' if has_categories else '❌'} Categories")

    # Show validation
    if has_article:
        issues = article.validate_for_publication()
        if issues:
            click.echo(f"\n⚠️  Issues:")
            for issue in issues:
                click.echo(f"     - {issue}")
        else:
            click.echo(f"\n✅ Ready for publication")


@cli.command()
@click.option('--series', help='Filter by series (e.g., ecommerce)')
def list(series: str):
    """
    List articles

    Shows all articles in artykuly/ directory.

    Example:
        blog-agent list
        blog-agent list --series ecommerce
    """
    project_root = Path.cwd()
    artykuly_dir = project_root / "artykuly"

    if not artykuly_dir.exists():
        click.echo("❌ No artykuly/ directory found")
        sys.exit(1)

    # Find all articles (directories with config.yaml)
    articles = []

    for config_path in artykuly_dir.rglob("config.yaml"):
        article_path = config_path.parent
        parts = article_path.relative_to(artykuly_dir).parts

        if len(parts) >= 3:
            article_series, article_silo, article_slug = parts[0], parts[1], parts[2]

            # Filter by series if specified
            if series and article_series != series:
                continue

            # Load config
            try:
                article_config = ArticleConfig.from_yaml(config_path)
                articles.append({
                    'series': article_series,
                    'silo': article_silo,
                    'slug': article_slug,
                    'title': article_config.title,
                    'path': article_path
                })
            except:
                pass

    if not articles:
        if series:
            click.echo(f"No articles found in series '{series}'")
        else:
            click.echo("No articles found")
        return

    # Display articles
    click.echo(f"\n📚 Articles ({len(articles)}):\n")

    current_series = None
    for article in sorted(articles, key=lambda x: (x['series'], x['silo'], x['slug'])):
        if current_series != article['series']:
            current_series = article['series']
            click.echo(f"\n{article['series']}/")

        click.echo(f"  {article['silo']}/{article['slug']}/")
        click.echo(f"    {article['title']}")


def main():
    """Main CLI entry point"""
    # Enable unbuffered output for real-time logs
    sys.stdout.reconfigure(line_buffering=True)
    sys.stderr.reconfigure(line_buffering=True)
    cli()


if __name__ == '__main__':
    main()

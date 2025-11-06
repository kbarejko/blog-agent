"""
CLI Commands

Click-based CLI for blog-agent.
"""
import click
from pathlib import Path
import sys

from ...core.domain.article import Article
from ...core.domain.config import ArticleConfig
from ...core.workflow.engine import WorkflowEngine
from ...core.factory import DependencyFactory


@click.group()
@click.version_option(version='1.0.0')
def cli():
    """
    Blog Agent - AI-powered article generation system

    Automatically generates blog articles with AI review and git versioning.
    """
    pass


@cli.command()
@click.option('--series', required=True, help='Series name (e.g., ecommerce, saas)')
@click.option('--silo', required=True, help='Silo name (e.g., operacje, platformy)')
@click.option('--slug', required=True, help='Article slug (e.g., bezpieczenstwo-rodo)')
@click.option('--title', required=True, help='Article title (H1)')
@click.option('--audience', required=True, help='Target audience')
@click.option('--tone', default='ekspercki, ale naturalny i rozmowny', help='Writing tone')
def init(series: str, silo: str, slug: str, title: str, audience: str, tone: str):
    """
    Initialize article structure

    Creates folder structure and config.yaml.

    Example:
        blog-agent init --series ecommerce --silo operacje --slug bezpieczenstwo-rodo --title "Bezpieczeństwo i RODO" --audience "Właściciele sklepów e-commerce"
    """
    # Build article path
    project_root = Path.cwd()
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
@click.option('--skip', multiple=True, help='Steps to skip (can be repeated)')
@click.option('--only', multiple=True, help='Only run these steps (can be repeated)')
def create(config_path: str, provider: str, skip: tuple, only: tuple):
    """
    Generate complete article

    Runs full workflow from outline to publication.

    Example:
        blog-agent create --config artykuly/ecommerce/operacje/bezpieczenstwo-rodo/config.yaml
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

    # Create factory and deps
    factory = DependencyFactory(project_root)
    deps = factory.create_deps(provider)

    # Create workflow engine
    workflow_config_path = factory.get_workflow_config_path()
    engine = WorkflowEngine(workflow_config_path)

    # Execute workflow
    try:
        article = engine.execute_workflow(
            article,
            deps,
            skip_steps=list(skip) if skip else None,
            only_steps=list(only) if only else None
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
@click.option('--path', 'article_path', required=True, type=click.Path(exists=True), help='Path to article directory')
def status(article_path: str):
    """
    Show article status

    Displays current state and progress.

    Example:
        blog-agent status --path artykuly/ecommerce/operacje/bezpieczenstwo-rodo/
    """
    article_path = Path(article_path)

    # Load config
    config_path = article_path / "config.yaml"
    if not config_path.exists():
        click.echo(f"❌ No config.yaml found in {article_path}")
        sys.exit(1)

    article_config = ArticleConfig.from_yaml(config_path)
    article = Article(path=article_path, config=article_config)

    # Check what exists
    has_outline = article.get_outline_path().exists()
    has_sections = len(list(article.get_sections_dir().glob("*.md"))) > 0
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
    cli()


if __name__ == '__main__':
    main()

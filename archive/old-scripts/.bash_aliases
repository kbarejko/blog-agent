# Aliasy dla Blog Agent
# Dodaj do ~/.bashrc: source ~/blog-agent/.bash_aliases

alias blog-new='~/blog-agent/new_article.sh'
alias blog-preview='~/blog-agent/preview.sh'
alias blog-publish='~/blog-agent/publish.sh'
alias blog-list='~/blog-agent/list_articles.sh'
alias blog-drafts='ls -lh ~/blog-agent/articles/drafts/'
alias blog-published='ls -lh ~/blog-agent/articles/published/'
alias blog-edit='micro'  # zmień na vim/nano jeśli wolisz
alias blog-agent='cd ~/blog-agent && python3 blog_agent.py'

# Funkcja do szybkiego generowania artykułu AI
blog-ai() {
    cd ~/blog-agent
    if [ -z "$1" ]; then
        echo "Użycie: blog-ai 'Temat artykułu'"
        echo "Przykład: blog-ai 'Jak zacząć z Docker'"
        return 1
    fi
    python3 -c "
from blog_agent import BlogAgent
import sys

agent = BlogAgent()
topic = ' '.join(sys.argv[1:])
print(f'🤖 Tworzę artykuł na temat: {topic}')
article = agent.create_article(topic=topic)
agent.save_article(article)
print('✅ Artykuł gotowy!')
" "$@"
}

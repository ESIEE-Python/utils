#!/bin/bash

# Répertoire contenant tous tes repos
BASE_DIR="./"
COMMIT_MSG="update"

# Fonction d'aide
show_help() {
    echo "Usage: $0 [OPTION]"
    echo "Options:"
    echo "  push           Add, commit and push all repos"
    echo "  pull           Pull latest changes from all repos"
    echo "  -h, --help     Show this help message"
}

# Analyser les arguments
ACTION=""
if [ $# -eq 0 ]; then
    echo "❌ Aucune option fournie"
    show_help
    exit 1
fi

case "$1" in
    push)
        ACTION="push"
        ;;
    pull)
        ACTION="pull"
        ;;
    -h|--help)
        show_help
        exit 0
        ;;
    *)
        echo "❌ Option inconnue: $1"
        show_help
        exit 1
        ;;
esac

echo "🚀 Action: $ACTION"

# Aller dans le répertoire parent
cd "$BASE_DIR" || exit 1

# Boucler sur chaque sous-dossier contenant un dépôt Git
for repo in */; do
    if [ -d "$repo/.git" ]; then
        echo "📂 Traitement du dépôt : $repo"
        cd "$repo" || continue

        case "$ACTION" in
            "push")
                git add .
                # Vérifier s'il y a des changements avant de commit
                if ! git diff --cached --quiet; then
                    git commit -m "$COMMIT_MSG"
                    git push
                    echo "✅ Ajouté, commité et poussé : $repo"
                else
                    echo "✅ Rien à committer dans $repo"
                fi
                ;;
            "pull")
                echo "⬇️ Récupération en cours..."
                if git pull; then
                    echo "✅ Mis à jour avec succès : $repo"
                else
                    echo "❌ Erreur lors de la récupération : $repo"
                fi
                ;;
        esac

        cd ..
    fi
done

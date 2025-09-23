#!/bin/bash

# Répertoire contenant tous tes repos
BASE_DIR="../repos/"
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

# Variable pour suivre s'il y a des changements
HAS_CHANGES=false

# Aller dans le répertoire parent
cd "$BASE_DIR" || exit 1

# Boucler sur chaque sous-dossier contenant un dépôt Git
for repo in */; do
    if [ -d "$repo/.git" ]; then
        echo
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
                    HAS_CHANGES=true
                else
                    echo "⚪ Rien à committer dans $repo"
                fi
                ;;
            "pull")
                echo "⬇️ Récupération en cours..."
                # Capturer l'état avant le pull
                BEFORE_COMMIT=$(git rev-parse HEAD)
                if git pull; then
                    AFTER_COMMIT=$(git rev-parse HEAD)
                    if [ "$BEFORE_COMMIT" != "$AFTER_COMMIT" ]; then
                        echo "✅ Changements récupérés dans $repo"
                        HAS_CHANGES=true
                    else
                        echo "⚪ Aucun changement à récupérer dans $repo"
                    fi
                else
                    echo "❌ Erreur lors de la récupération : $repo"
                fi
                ;;
        esac

        cd ..
    fi
done

# Message final basé sur s'il y a eu des changements
echo ""
if [ "$HAS_CHANGES" = true ]; then
    case "$ACTION" in
        "push")
            echo "🎉 Opération terminée ! Des changements ont été poussés vers les dépôts distants."
            ;;
        "pull")
            echo "🎉 Opération terminée ! Des changements ont été récupérés depuis les dépôts distants."
            ;;
    esac
else
    case "$ACTION" in
        "push")
            echo "😴 Aucun changement à pousser. Tous les dépôts sont déjà à jour."
            ;;
        "pull")
            echo "😴 Aucun changement à récupérer. Tous les dépôts sont déjà à jour."
            ;;
    esac
fi

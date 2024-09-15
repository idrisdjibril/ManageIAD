#!/bin/bash

# Configuration de la base de données
DBNAME="interoperabilite"
DBUSER="landry"
DBPASSWORD="12345"
DBTABLE="DHSI2"
WATCH_DIRECTORY="/var/crvs_dhis2_save"
LOGFILE="/Bureau/projet_stage/téléchargements/processed_files.log"

# Fonction pour vérifier si un fichier a déjà été importé
file_already_processed() {
    grep -q "$1" "$LOGFILE"
    return $?
}

# Fonction pour marquer un fichier comme traité
mark_file_as_processed() {
    echo "$1" >> "$LOGFILE"
}

# Fonction pour générer un nom de colonne unique
generate_unique_column_name() {
    local col_name="$1"
    local index=1
    local new_name="$col_name"
    
    while [[ " ${COLUMN_NAMES[@]} " =~ " ${new_name} " ]]; do
        new_name="${col_name}_${index}"
        index=$((index + 1))
    done
    
    echo "$new_name"
}

# Fonction pour traiter un fichier CSV
process_csv_file() {
    local FILEPATH="$1"
    local FILENAME=$(basename "$FILEPATH")

    if file_already_processed "$FILENAME"; then
        echo "Le fichier $FILENAME a déjà été importé. Ignoré."
        return
    fi

    echo "Traitement du fichier $FILENAME..."

    # Lire la première ligne du fichier pour détecter les colonnes
    HEADER=$(head -n 1 "$FILEPATH")

    # Normaliser les en-têtes en remplaçant les délimiteurs par des virgules
    NORMALIZED_HEADER=$(echo "$HEADER" | sed 's/[;#|]/,/g')

    # Nettoyer les noms de colonnes pour les rendre compatibles avec PostgreSQL
    IFS=',' read -ra RAW_COLUMNS <<< "$NORMALIZED_HEADER"
    COLUMN_NAMES=()
    CLEANED_HEADER=""
    for col in "${RAW_COLUMNS[@]}"; do
        cleaned_col=$(echo "$col" | sed "s/[^a-zA-Z0-9]/_/g")
        unique_col=$(generate_unique_column_name "$cleaned_col")
        COLUMN_NAMES+=("$unique_col")
        CLEANED_HEADER+="$unique_col,"
    done
    CLEANED_HEADER=${CLEANED_HEADER%,}

    # Afficher les colonnes trouvées
    echo "Colonnes trouvées :"
    for col in "${COLUMN_NAMES[@]}"; do
        echo "  $col"
    done

    # Créer une table PostgreSQL basée sur les en-têtes
    COLUMNS=$(for col in "${COLUMN_NAMES[@]}"; do
        echo "$col TEXT"
    done | paste -sd,)

    CREATE_TABLE_QUERY="CREATE TABLE IF NOT EXISTS $DBTABLE ($COLUMNS);"
    PGPASSWORD="$DBPASSWORD" psql -U "$DBUSER" -d "$DBNAME" -c "$CREATE_TABLE_QUERY"

    # Créer un fichier temporaire pour le COPY
    TEMP_FILE=$(mktemp)
    tail -n +2 "$FILEPATH" | sed 's/[;#|]/,/g' > "$TEMP_FILE"

    # Importer les données dans la table PostgreSQL
    PGPASSWORD="$DBPASSWORD" psql -U "$DBUSER" -d "$DBNAME" -c "\COPY $DBTABLE ($CLEANED_HEADER) FROM '$TEMP_FILE' WITH CSV DELIMITER ',' NULL AS ''"

    # Supprimer le fichier temporaire
    rm "$TEMP_FILE"

    # Marquer le fichier comme traité
    mark_file_as_processed "$FILENAME"

    echo "Importation du fichier $FILENAME terminée."
}

# Fonction pour traiter un dossier daté
process_dated_folder() {
    local FOLDER="$1"
    local CSV_FILE="$FOLDER/csv/formulaire_de_declaration_de_naissances_fosa_$(basename "$FOLDER").csv"
    
    if [ -f "$CSV_FILE" ]; then
        process_csv_file "$CSV_FILE"
    else
        echo "Fichier CSV non trouvé dans $FOLDER"
    fi
}

# Fonction pour traiter les dossiers existants et surveiller les nouveaux
process_and_monitor_folders() {
    # Traiter les dossiers existants
    for folder in "$WATCH_DIRECTORY"/????-??-??; do
        if [ -d "$folder" ]; then
            process_dated_folder "$folder"
        fi
    done

    # Surveiller les nouveaux dossiers
    inotifywait -m -e create --format "%w%f" "$WATCH_DIRECTORY" | while read NEWDIR
    do
        if [[ -d "$NEWDIR" && "$NEWDIR" =~ [0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
            echo "Nouveau dossier détecté : $NEWDIR"
            process_dated_folder "$NEWDIR"
        fi
    done
}

# Créer le fichier de log s'il n'existe pas
touch "$LOGFILE"

# Lancer le traitement et la surveillance
process_and_monitor_folders
set shell := ["bash", "-eu", "-o", "pipefail", "-c"]

certs_dir := "certs"
plugin_name := "rosreestr-search-qgis-plugin"
root_url := "https://gu-st.ru/content/Other/doc/russian_trusted_root_ca.cer"
subca_url := "http://nuc-cdp.digital.gov.ru/cdp/subca_ssl_rsa2024.crt"

default:
    @just --list

download-certs:
    mkdir -p "{{certs_dir}}"
    curl -fsSL "{{root_url}}" -o "{{certs_dir}}/russian_trusted_root_ca.download"
    curl -fsSL "{{subca_url}}" -o "{{certs_dir}}/subca_ssl_rsa2024.download"
    openssl x509 -in "{{certs_dir}}/russian_trusted_root_ca.download" -out "{{certs_dir}}/russian_trusted_root_ca.pem" || openssl x509 -inform DER -in "{{certs_dir}}/russian_trusted_root_ca.download" -out "{{certs_dir}}/russian_trusted_root_ca.pem"
    openssl x509 -in "{{certs_dir}}/subca_ssl_rsa2024.download" -out "{{certs_dir}}/subca_ssl_rsa2024.pem" || openssl x509 -inform DER -in "{{certs_dir}}/subca_ssl_rsa2024.download" -out "{{certs_dir}}/subca_ssl_rsa2024.pem"
    cat "{{certs_dir}}/russian_trusted_root_ca.pem" "{{certs_dir}}/subca_ssl_rsa2024.pem" > "{{certs_dir}}/nspd-ca-bundle.pem"
    rm -f "{{certs_dir}}/russian_trusted_root_ca.download" "{{certs_dir}}/subca_ssl_rsa2024.download"
    openssl verify -CAfile "{{certs_dir}}/russian_trusted_root_ca.pem" "{{certs_dir}}/subca_ssl_rsa2024.pem"
    openssl x509 -in "{{certs_dir}}/russian_trusted_root_ca.pem" -noout -subject -issuer -fingerprint -sha256 -dates
    openssl x509 -in "{{certs_dir}}/subca_ssl_rsa2024.pem" -noout -subject -issuer -fingerprint -sha256 -dates

package output="dist/rosreestr-search-qgis-plugin.zip":
    #!/usr/bin/env bash
    set -euo pipefail
    mkdir -p "$(dirname "{{output}}")"
    tmpdir="$(mktemp -d)"
    trap 'rm -rf "$tmpdir"' EXIT
    plugindir="$tmpdir/{{plugin_name}}"

    git ls-files -z --cached | while IFS= read -r -d '' path; do
        if git check-attr export-ignore -- "$path" | grep -q ': export-ignore: set$'; then
            continue
        fi

        mkdir -p "$plugindir/$(dirname "$path")"
        cp "$path" "$plugindir/$path"
    done

    (cd "$tmpdir" && zip -qr "$OLDPWD/{{output}}" "{{plugin_name}}")
    unzip -tq "{{output}}"
    echo "Created {{output}}"

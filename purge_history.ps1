
$passwords = @(
    "!!Anaconda@1981##",
    "hRM3ra4vHy9Uy78c",
    "wSdypQurdXqA4w95",
    "123456`""
)

# Join passwords for regex correctly
$escaped = @()
foreach ($p in $passwords) {
    $escaped += [Regex]::Escape($p)
}
$regex = "(" + ($escaped -join "|") + ")"

echo "Regex pattern to clean: $regex"

# Create a cleanup script to be called by tree-filter
$cleanupScript = @"
`$regex = '$regex'
Get-ChildItem -Recurse -File | ForEach-Object {
    `$file = `$_.FullName
    # Skip .git directory and the cleanup script itself
    if (`$file -match '\\.git\\') { return }
    if (`$file -match 'cleanup_all.ps1') { return }
    if (`$file -match 'purge_history.ps1') { return }
    
    try {
        `$content = Get-Content `$file -Raw -ErrorAction SilentlyContinue
        if (`$content -and (`$content -match `$regex)) {
             `$content -replace `$regex, 'REPLACED_PASSWORD' | Set-Content `$file
        }
    } catch {}
}
"@

$cleanupPath = "c:\Users\meyss\Downloads\Airflow-Jenkins-Postgresql-Migration-CICD\cleanup_all.ps1"
$cleanupScript | Set-Content $cleanupPath

# Run git filter-branch
# Squelch warning and run
$env:FILTER_BRANCH_SQUELCH_WARNING = "1"
git filter-branch --force --tree-filter "powershell -File '$cleanupPath'" HEAD

# Cleanup will be done manually after verification

$regex = '(!!Anaconda@1981\#\#|hRM3ra4vHy9Uy78c|wSdypQurdXqA4w95|123456")'
Get-ChildItem -Recurse -File | ForEach-Object {
    $file = $_.FullName
    # Skip .git directory and the cleanup script itself
    if ($file -match '\\.git\\') { return }
    if ($file -match 'cleanup_all.ps1') { return }
    if ($file -match 'purge_history.ps1') { return }
    
    try {
        $content = Get-Content $file -Raw -ErrorAction SilentlyContinue
        if ($content -and ($content -match $regex)) {
             $content -replace $regex, 'REPLACED_PASSWORD' | Set-Content $file
        }
    } catch {}
}

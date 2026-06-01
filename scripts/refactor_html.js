const fs = require('fs');
const path = require('path');

function refactorHtmlFiles() {
    const pagesDir = 'pages';
    const rootDir = '.';
    
    // 1. Refactor root 404.html
    const root404 = path.join(rootDir, '404.html');
    if (fs.existsSync(root404)) {
        let content = fs.readFileSync(root404, 'utf8');
        content = content.replace(/assets\/js\/tailwind-config\.js/g, 'configs/tailwind-config.js');
        fs.writeFileSync(root404, content, 'utf8');
        console.log("Refactored root 404.html");
    }

    // 2. Refactor pages/
    const files = fs.readdirSync(pagesDir);
    const inlineScriptPattern = /<script\s+id="tailwind-config">[\s\S]*?<\/script>/g;
    
    files.forEach(filename => {
        if (filename.endsWith('.html')) {
            const filepath = path.join(pagesDir, filename);
            let content = fs.readFileSync(filepath, 'utf8');
            const original = content;
            
            // Replace inline tailwind configs
            if (inlineScriptPattern.test(content)) {
                content = content.replace(inlineScriptPattern, '<script src="../configs/tailwind-config.js"></script>');
                console.log(`Removed inline tailwind config in ${filename}`);
            }
            
            // Replace regular scripts
            content = content.split('../assets/js/tailwind-config.js').join('../configs/tailwind-config.js');
            content = content.split('assets/js/tailwind-config.js').join('../configs/tailwind-config.js');
            
            if (content !== original) {
                fs.writeFileSync(filepath, content, 'utf8');
                console.log(`Updated ${filename}`);
            }
        }
    });
}

refactorHtmlFiles();

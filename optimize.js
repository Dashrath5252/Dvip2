// WordPress Style Auto Optimizer - Single File
const sharp = require('sharp');
const fs = require('fs');

console.log('🚀 Auto Optimizer Starting...\n');

// Check images
const images = ['dvip1.webp', 'dvip2.webp', 'dvip3.webp', 'dvip4.webp', 'dvipicon512.webp'];
const found = images.filter(img => fs.existsSync(img));

if (found.length === 0) {
    console.log('❌ No images found!');
    process.exit(1);
}

console.log(`✅ Found ${found.length} images\n`);

// Process each image
found.forEach(img => {
    console.log(`🔄 ${img}`);
    const name = img.replace('.webp', '');
    
    if (img.includes('dvipicon')) {
        // Icon - 512×512
        sharp(img).resize(512,512).png({quality:95}).toFile(`${name}_google.png`);
        sharp(img).resize(512,512).webp({quality:90}).toFile(`${name}_optimized.webp`);
        console.log(`   ✅ ${name}_google.png (512×512 PNG)`);
        console.log(`   ✅ ${name}_optimized.webp (512×512 WebP)`);
    } else {
        // Main images - 450×800
        sharp(img).resize(675,1200).png({quality:95}).toFile(`${name}_google.png`);
        sharp(img).resize(450,800).webp({quality:90}).toFile(`${name}_optimized.webp`);
        console.log(`   ✅ ${name}_google.png (675×1200 PNG)`);
        console.log(`   ✅ ${name}_optimized.webp (450×800 WebP)`);
    }
    console.log('');
});

console.log('🎉 Done! Use:');
console.log('- PNG files for Google (_google.png)');
console.log('- WebP files for website (_optimized.webp)');

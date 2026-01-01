// WordPress Style Auto Image Optimizer - EXISTING IMAGES ONLY
const sharp = require('sharp');
const fs = require('fs');

console.log('🔄 Optimizing EXISTING images only...\n');

// SIRF YE 5 IMAGES OPTIMIZE KARO
const EXISTING_IMAGES = [
  'dvip1.webp',
  'dvip2.webp', 
  'dvip3.webp',
  'dvip4.webp',
  'dvipicon512.webp'
];

// Quality settings
const QUALITY = {
  GOOGLE_PNG: 95,      // Google ke liye PNG quality
  WEBSITE_WEBP: 90,    // Website ke liye WebP quality
  THUMBNAIL: 85        // Thumbnail quality
};

// Check which images exist
const foundImages = EXISTING_IMAGES.filter(img => fs.existsSync(img));

if (foundImages.length === 0) {
  console.log('❌ No existing images found!');
  process.exit(1);
}

console.log(`✅ Found ${foundImages.length}/5 existing images:\n`);
foundImages.forEach(img => console.log(`   • ${img}`));
console.log('');

// Process ONLY existing images
foundImages.forEach(image => {
  console.log(`🎯 Optimizing: ${image}`);
  const name = image.replace('.webp', '');
  
  if (image.includes('dvipicon')) {
    // Icon optimization
    sharp(image)
      .resize(512, 512)
      .png({ quality: QUALITY.GOOGLE_PNG })
      .toFile(`${name}_google.png`)
      .then(() => console.log(`   ✅ ${name}_google.png (512×512 PNG)`));
    
    sharp(image)
      .resize(512, 512)
      .webp({ quality: QUALITY.WEBSITE_WEBP })
      .toFile(`${name}_optimized.webp`)
      .then(() => console.log(`   ✅ ${name}_optimized.webp (512×512 WebP)`));
      
  } else {
    // Main images optimization
    sharp(image)
      .resize(675, 1200, { fit: 'cover', position: 'center' })
      .png({ quality: QUALITY.GOOGLE_PNG })
      .toFile(`${name}_google.png`)
      .then(() => console.log(`   ✅ ${name}_google.png (675×1200 PNG)`));
    
    sharp(image)
      .resize(450, 800, { fit: 'cover' })
      .webp({ quality: QUALITY.WEBSITE_WEBP })
      .toFile(`${name}_optimized.webp`)
      .then(() => console.log(`   ✅ ${name}_optimized.webp (450×800 WebP)`));
    
    // Optional thumbnail
    sharp(image)
      .resize(225, 400, { fit: 'cover' })
      .webp({ quality: QUALITY.THUMBNAIL })
      .toFile(`${name}_thumb.webp`)
      .then(() => console.log(`   ✅ ${name}_thumb.webp (225×400 WebP)`));
  }
  
  console.log('');
});

console.log('='.repeat(50));
console.log('🎉 EXISTING IMAGES OPTIMIZATION COMPLETE!');
console.log('='.repeat(50));
console.log('\n📁 GENERATED FILES (Existing images se):');
console.log('├── [name]_google.png     → Google Search ke liye');
console.log('├── [name]_optimized.webp → Website ke liye');
console.log('└── [name]_thumb.webp     → Thumbnail (optional)');
console.log('\n💡 Koi nayi image add nahi ki gayi!');

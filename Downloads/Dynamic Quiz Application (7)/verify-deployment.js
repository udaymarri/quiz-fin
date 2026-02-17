#!/usr/bin/env node

/**
 * Pre-Deployment Verification Script
 * Run this before deploying to catch any issues
 * 
 * Usage: node verify-deployment.js
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

// Polyfill for __dirname in ESM
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

console.log('\n🔍 QuizMaster Pro - Pre-Deployment Verification\n');
console.log('='.repeat(50));

let hasErrors = false;
let hasWarnings = false;

// Files that must exist
const requiredFiles = [
  'index.html',
  'vercel.json',
  'package.json',
  'vite.config.ts',
  'src/main.tsx',
  'src/app/App.tsx',
  '.gitignore'
];

// Check required files
console.log('\n📁 Checking Required Files...\n');
requiredFiles.forEach(file => {
  const exists = fs.existsSync(path.join(__dirname, file));
  if (exists) {
    console.log(`   ✅ ${file}`);
  } else {
    console.log(`   ❌ ${file} - MISSING!`);
    hasErrors = true;
  }
});

// Check package.json scripts
console.log('\n📦 Checking package.json scripts...\n');
try {
  const pkg = JSON.parse(fs.readFileSync(path.join(__dirname, 'package.json'), 'utf8'));

  const requiredScripts = ['dev', 'build', 'preview'];
  requiredScripts.forEach(script => {
    if (pkg.scripts && pkg.scripts[script]) {
      console.log(`   ✅ ${script}: ${pkg.scripts[script]}`);
    } else {
      console.log(`   ❌ ${script} script missing!`);
      hasErrors = true;
    }
  });

  // Check dependencies
  console.log('\n📚 Checking Critical Dependencies...\n');
  const criticalDeps = ['react', 'react-dom', 'vite', 'motion', 'lucide-react', 'recharts'];
  criticalDeps.forEach(dep => {
    const exists = (pkg.dependencies && pkg.dependencies[dep]) ||
      (pkg.devDependencies && pkg.devDependencies[dep]) ||
      (pkg.peerDependencies && pkg.peerDependencies[dep]);
    if (exists) {
      console.log(`   ✅ ${dep}`);
    } else {
      console.log(`   ⚠️  ${dep} not found in dependencies`);
      hasWarnings = true;
    }
  });

} catch (error) {
  console.log(`   ❌ Error reading package.json: ${error.message}`);
  hasErrors = true;
}

// Check vercel.json configuration
console.log('\n⚙️  Checking vercel.json configuration...\n');
try {
  const vercelConfig = JSON.parse(fs.readFileSync(path.join(__dirname, 'vercel.json'), 'utf8'));

  if (vercelConfig.rewrites && vercelConfig.rewrites.length > 0) {
    console.log('   ✅ SPA routing configured');
  } else {
    console.log('   ⚠️  No rewrites found - may cause 404 on refresh');
    hasWarnings = true;
  }

  if (vercelConfig.buildCommand) {
    console.log(`   ✅ Build command: ${vercelConfig.buildCommand}`);
  }

  if (vercelConfig.outputDirectory) {
    console.log(`   ✅ Output directory: ${vercelConfig.outputDirectory}`);
  }

} catch (error) {
  console.log(`   ⚠️  Could not read vercel.json: ${error.message}`);
  hasWarnings = true;
}

// Check .gitignore
console.log('\n🚫 Checking .gitignore...\n');
try {
  const gitignore = fs.readFileSync(path.join(__dirname, '.gitignore'), 'utf8');

  const mustIgnore = ['node_modules', 'dist', '.env'];
  mustIgnore.forEach(item => {
    if (gitignore.includes(item)) {
      console.log(`   ✅ Ignoring ${item}`);
    } else {
      console.log(`   ⚠️  ${item} not in .gitignore`);
      hasWarnings = true;
    }
  });

} catch (error) {
  console.log(`   ⚠️  Could not read .gitignore: ${error.message}`);
  hasWarnings = true;
}

// Check for large files
console.log('\n💾 Checking for large files...\n');
try {
  const { execSync } = await import('node:child_process');

  // This will fail gracefully if git is not initialized
  try {
    execSync('git rev-parse --git-dir', { stdio: 'ignore' });
    console.log('   ✅ Git repository initialized');
  } catch {
    console.log('   ⚠️  Git not initialized - run: git init');
    hasWarnings = true;
  }

} catch (error) {
  // Git might not be available
  console.log('   ℹ️  Could not check git status');
}

// Check node_modules size (warning if too large)
console.log('\n📊 Checking project size...\n');
try {
  const getDirectorySize = (dir) => {
    if (!fs.existsSync(dir)) return 0;

    let size = 0;
    const files = fs.readdirSync(dir);

    files.forEach(file => {
      const filePath = path.join(dir, file);
      const stats = fs.statSync(filePath);

      if (stats.isDirectory()) {
        size += getDirectorySize(filePath);
      } else {
        size += stats.size;
      }
    });

    return size;
  };

  const srcSize = getDirectorySize(path.join(__dirname, 'src'));
  const srcSizeMB = (srcSize / (1024 * 1024)).toFixed(2);

  console.log(`   ℹ️  Source code size: ${srcSizeMB} MB`);

  if (srcSize > 50 * 1024 * 1024) { // 50MB
    console.log('   ⚠️  Source code is quite large - consider optimization');
    hasWarnings = true;
  } else {
    console.log('   ✅ Source code size is reasonable');
  }

} catch (error) {
  console.log('   ℹ️  Could not calculate project size');
}

// Final summary
console.log('\n' + '='.repeat(50));
console.log('\n📋 Verification Summary:\n');

if (!hasErrors && !hasWarnings) {
  console.log('   🎉 All checks passed! Ready to deploy!\n');
  console.log('   Next steps:');
  console.log('   1. Run: npm run build');
  console.log('   2. Test: npm run preview');
  console.log('   3. Deploy to Vercel\n');
  process.exit(0);
} else if (hasErrors) {
  console.log('   ❌ Found critical errors that must be fixed\n');
  console.log('   Please resolve the errors above before deploying.\n');
  process.exit(1);
} else if (hasWarnings) {
  console.log('   ⚠️  Found warnings - review them before deploying\n');
  console.log('   You can proceed, but fixing warnings is recommended.\n');
  process.exit(0);
}

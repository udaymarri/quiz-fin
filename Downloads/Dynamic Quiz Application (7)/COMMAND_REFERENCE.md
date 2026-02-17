# 🎯 Vercel Deployment - Command Cheat Sheet

## 📦 Local Development

```bash
# Install dependencies
npm install

# Start development server (http://localhost:5173)
npm run dev

# Build for production
npm run build

# Preview production build (http://localhost:4173)
npm run preview

# Verify deployment readiness
node verify-deployment.js
```

---

## 🐙 Git Commands

```bash
# Initialize repository
git init

# Check status
git status

# Stage all files
git add .

# Commit with message
git commit -m "Your message here"

# Add remote repository (replace USERNAME and REPO)
git remote add origin https://github.com/USERNAME/REPO.git

# Rename branch to main
git branch -M main

# Push to GitHub
git push -u origin main

# Push updates (after first push)
git push
```

---

## 🔄 Update Workflow

```bash
# 1. Make changes to your code

# 2. Stage and commit
git add .
git commit -m "Description of changes"

# 3. Push to GitHub (Vercel auto-deploys!)
git push

# That's it! Vercel will auto-deploy in 2-3 minutes
```

---

## 🌐 Vercel CLI (Optional)

```bash
# Install Vercel CLI globally
npm install -g vercel

# Login to Vercel
vercel login

# Deploy preview
vercel

# Deploy to production
vercel --prod

# View logs
vercel logs

# List deployments
vercel ls

# Open project in browser
vercel open

# Link project to existing Vercel project
vercel link

# Pull environment variables
vercel env pull

# Remove project
vercel remove
```

---

## 🔍 Debugging

```bash
# Check for errors
npm run build

# Clear cache and reinstall
rm -rf node_modules package-lock.json dist
npm install

# Check node and npm versions
node --version
npm --version

# List outdated packages
npm outdated

# Update packages
npm update
```

---

## 📊 Useful One-Liners

```bash
# Count lines of code
find src -name '*.tsx' -o -name '*.ts' | xargs wc -l

# Find large files
find . -type f -size +1M

# Check git remote
git remote -v

# View recent commits
git log --oneline -5

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Discard all local changes
git reset --hard HEAD
```

---

## 🚀 Complete Deployment Flow

```bash
# 1. Verify project
node verify-deployment.js

# 2. Test build
npm install && npm run build && npm run preview

# 3. Initialize Git (if not done)
git init

# 4. Commit everything
git add .
git commit -m "Initial commit: Ready for deployment"

# 5. Create GitHub repo (on github.com)
# Then link and push:
git remote add origin https://github.com/YOUR-USERNAME/quizmaster-pro.git
git branch -M main
git push -u origin main

# 6. Deploy on Vercel (via dashboard)
# Go to vercel.com → Import Project → Deploy
```

---

## 📝 Environment Variables

```bash
# Using Vercel CLI to manage env vars

# Add variable
vercel env add VARIABLE_NAME

# Pull variables to local
vercel env pull

# List variables
vercel env ls

# Remove variable
vercel env rm VARIABLE_NAME
```

---

## 🎯 Quick Fixes

```bash
# Fix: "Module not found"
npm install missing-package
git add package.json package-lock.json
git commit -m "Add missing dependency"
git push

# Fix: "Build failed"
npm run build  # Test locally first
# Check error messages
# Fix issues, then push

# Fix: "Git push rejected"
git pull origin main
git push origin main

# Fix: "Vercel not deploying"
# Manual trigger: Vercel Dashboard → Deployments → Redeploy
```

---

## 📱 Mobile Testing

```bash
# Get local IP
# macOS/Linux:
ipconfig getifaddr en0

# Windows:
ipconfig

# Access from phone:
# http://YOUR-LOCAL-IP:5173
```

---

## 🔐 Security

```bash
# Check for security issues
npm audit

# Fix automatically
npm audit fix

# Fix with breaking changes
npm audit fix --force
```

---

## 📦 Package Management

```bash
# Install specific version
npm install package@version

# Install as dev dependency
npm install --save-dev package

# Uninstall package
npm uninstall package

# Update specific package
npm update package

# Clean install
rm -rf node_modules package-lock.json
npm install
```

---

## 🎨 Useful Shortcuts

| Command | Shortcut | Description |
|---------|----------|-------------|
| `git status` | `git st` | (with alias) |
| `git commit -m` | `git cm` | (with alias) |
| `git add .` | `ga .` | (with alias) |
| `Ctrl+C` | - | Stop dev server |
| `npm run dev` | `npm start` | (if configured) |

---

## 🔗 Quick Links

- **Vercel Dashboard:** https://vercel.com/dashboard
- **GitHub:** https://github.com
- **Vercel Docs:** https://vercel.com/docs
- **Vercel Status:** https://www.vercel-status.com

---

## 💡 Pro Tips

```bash
# Create git aliases for faster workflow
git config --global alias.st status
git config --global alias.cm "commit -m"
git config --global alias.ac "!git add . && git commit -m"
git config --global alias.p push

# Then use:
git st          # instead of git status
git cm "msg"    # instead of git commit -m "msg"
git ac "msg"    # add all and commit
git p          # instead of git push
```

---

## 🎯 Daily Workflow

```bash
# Morning: Start working
git pull                    # Get latest changes
npm run dev                # Start dev server

# During: Make changes
# ... code code code ...

# Evening: Push changes
git add .
git commit -m "Today's work"
git push

# Vercel automatically deploys! ✨
```

---

## 📊 Stats & Info

```bash
# Project stats
npm ls                     # List installed packages
npm ls --depth=0          # Top-level packages only

# Bundle size
npm run build
du -sh dist/              # Check dist folder size

# Dependencies count
npm ls | wc -l
```

---

**Keep this handy during deployment! 📌**

**Print or save this reference for quick access! 💾**

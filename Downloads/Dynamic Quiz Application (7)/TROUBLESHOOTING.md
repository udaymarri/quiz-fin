# 🔧 Vercel Deployment Troubleshooting Guide

Quick solutions to common deployment issues.

---

## 🚨 Build Failed Errors

### Error: "Module not found: Can't resolve 'xyz'"

**Cause:** Missing dependency

**Solution:**
```bash
# Install the missing package
npm install xyz --save

# Commit and push
git add package.json package-lock.json
git commit -m "Add missing dependency"
git push
```

---

### Error: "Build script not found"

**Cause:** Missing `build` script in package.json

**Solution:**
Check `package.json` has:
```json
{
  "scripts": {
    "build": "vite build"
  }
}
```

If missing, add it and push changes.

---

### Error: "Cannot find module '@/app/...'"

**Cause:** Path alias not configured

**Solution:**
Check `vite.config.ts` has:
```typescript
resolve: {
  alias: {
    '@': path.resolve(__dirname, './src'),
  },
},
```

---

### Error: "Build exceeded maximum duration"

**Cause:** Build taking too long (>15 minutes on free plan)

**Solutions:**
1. Remove unused dependencies
2. Optimize build process
3. Check for infinite loops in build scripts
4. Upgrade to paid plan if needed

---

## 🔗 Routing & 404 Errors

### Issue: Page works initially but 404 on refresh

**Cause:** SPA routing not configured

**Solution:**
Ensure `vercel.json` has:
```json
{
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

✅ Already included in your project!

---

### Issue: Assets not loading (images, fonts, etc.)

**Cause:** Incorrect paths or missing public directory

**Solutions:**
1. Check image paths are correct
2. Use `/` for absolute paths from public
3. Ensure assets are in `public/` or imported in code

---

## 🌐 Domain & SSL Issues

### Issue: "Domain is not configured correctly"

**Solutions:**

**For Vercel subdomain:**
- Just wait 2-3 minutes for DNS propagation

**For custom domain:**
1. Verify DNS settings at your registrar
2. Ensure A record points to: `76.76.21.21`
3. Ensure CNAME points to: `cname.vercel-dns.com`
4. Wait up to 48 hours for DNS propagation

---

### Issue: "SSL certificate pending"

**Solution:**
- Wait 5-10 minutes after domain configuration
- Vercel auto-generates SSL certificates
- If stuck > 30 minutes, remove and re-add domain

---

## 🔐 Environment Variables

### Issue: Environment variables not working

**Solutions:**

1. **Check variable names**
   - Must start with `VITE_` to be accessible in code
   - Example: `VITE_API_KEY`

2. **Add to all environments**
   - Production
   - Preview  
   - Development

3. **Redeploy after adding**
   - Deployments → Click ⋯ → Redeploy
   - OR: Push a new commit

4. **Access correctly in code**
```typescript
// Correct:
const apiKey = import.meta.env.VITE_API_KEY;

// Wrong:
const apiKey = process.env.VITE_API_KEY;
```

---

## 📦 Dependency Issues

### Issue: "Peer dependency warnings"

**Solution:**
Usually safe to ignore, but if build fails:
```bash
npm install --legacy-peer-deps
```

Or update to compatible versions.

---

### Issue: "Package size too large"

**Solutions:**
1. Remove unused dependencies:
```bash
npm uninstall unused-package
```

2. Check for accidentally committed `node_modules`:
```bash
# Should be in .gitignore
echo "node_modules" >> .gitignore
git rm -r --cached node_modules
git commit -m "Remove node_modules from git"
```

---

## ⚡ Performance Issues

### Issue: "Build is slow"

**Solutions:**
1. Use `.vercelignore` to skip unnecessary files:
```
# .vercelignore
*.md
docs/
tests/
```

2. Optimize dependencies:
```bash
# Remove dev dependencies from production
npm prune --production
```

---

### Issue: "Site loads slowly"

**Solutions:**
1. **Enable Vercel Speed Insights**
   - Dashboard → Speed Insights → Enable

2. **Optimize images**
   - Use WebP format
   - Compress images
   - Use appropriate sizes

3. **Code splitting** (if not already done by Vite)
   - Vite handles this automatically

4. **Check bundle size**
```bash
npm run build
# Check dist/ folder size
```

---

## 🔄 Git & GitHub Issues

### Issue: "Failed to push to GitHub"

**Solutions:**

**Authentication error:**
```bash
# Use HTTPS with token or SSH
git remote set-url origin https://github.com/username/repo.git
```

**Rejected push:**
```bash
# Pull first
git pull origin main
# Then push
git push origin main
```

**Large file error:**
```bash
# Remove from git history
git rm --cached large-file.zip
git commit -m "Remove large file"
```

---

### Issue: "Vercel not detecting new pushes"

**Solutions:**
1. Check GitHub integration:
   - Vercel Dashboard → Settings → Git
   - Verify repository is connected

2. Manual redeploy:
   - Deployments → Click ⋯ → Redeploy

3. Reconnect repository:
   - Settings → Git → Disconnect → Reconnect

---

## 🎨 UI/Styling Issues

### Issue: "Styles not applying"

**Solutions:**
1. Check Tailwind config:
```javascript
// vite.config.ts should have
import tailwindcss from '@tailwindcss/vite'

plugins: [tailwindcss()]
```

2. Verify CSS imports:
```typescript
// main.tsx should import
import './styles/index.css'
```

3. Clear cache and rebuild:
```bash
rm -rf node_modules dist
npm install
npm run build
```

---

### Issue: "Animations not working"

**Solution:**
Check Motion (Framer Motion) is imported correctly:
```typescript
import { motion } from 'motion/react'
// NOT from 'framer-motion'
```

---

## 🔍 Debugging Tips

### View Build Logs

1. Vercel Dashboard → Deployments
2. Click your deployment
3. View detailed logs
4. Look for error messages

### Test Locally First

Always test production build locally:
```bash
# Build
npm run build

# Test production build
npm run preview

# Open http://localhost:4173
```

### Check Vercel Status

Sometimes it's Vercel, not you:
- Visit: [vercel-status.com](https://www.vercel-status.com/)
- Check for ongoing incidents

---

## 📞 Still Need Help?

### Official Resources

1. **Vercel Docs**
   - [vercel.com/docs](https://vercel.com/docs)
   - Comprehensive documentation

2. **Vercel Support**
   - [vercel.com/support](https://vercel.com/support)
   - Submit ticket (Pro plans)

3. **Community**
   - [GitHub Discussions](https://github.com/vercel/vercel/discussions)
   - [Discord](https://discord.gg/vercel)

### Before Asking for Help

Include this info:
- Deployment URL or ID
- Full error message
- Build logs
- What you've tried
- Browser/device info (if relevant)

---

## ✅ Prevention Checklist

Avoid issues by checking before each deployment:

- [ ] Run `npm run build` locally - succeeds?
- [ ] Run `npm run preview` - works correctly?
- [ ] All tests passing?
- [ ] `.gitignore` includes `node_modules/`, `dist/`, `.env`
- [ ] No sensitive data in code
- [ ] Environment variables added to Vercel
- [ ] DNS configured (if using custom domain)

---

## 🎯 Quick Fixes Summary

| Problem | Quick Fix |
|---------|-----------|
| Build fails | Run locally first: `npm run build` |
| 404 on refresh | Check `vercel.json` rewrites |
| Env vars not working | Redeploy after adding them |
| Slow build | Add `.vercelignore` |
| Domain not working | Wait for DNS (up to 48h) |
| Git push rejected | `git pull` first |
| Styles missing | Check Tailwind config |

---

## 🚀 Pro Tips

1. **Always test locally before deploying**
2. **Check build logs first** - most errors are there
3. **Use Vercel CLI for detailed logs**: `vercel logs`
4. **Enable preview deployments** for testing
5. **Set up branch deployments** for staging
6. **Monitor Vercel Analytics** for issues

---

**Remember: 99% of deployment issues are fixable! 💪**

**Need more help? Check the full DEPLOYMENT_GUIDE.md**

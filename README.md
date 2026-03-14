# 🐠 MVS AQUA - Full Stack Django Website
# WhatsApp: +91 9490255775 | Instagram: @Mvs_aqua

================================================================
  READ THIS FIRST — WHY YOU SAW ERRORS
================================================================

ERROR 1: "No module named 'django'"
   REASON : Django is not installed on your PC yet
   FIX    : Run INSTALL_AND_RUN.bat (see below)

ERROR 2: HTML file shows {%block%} raw code in browser
   REASON : You opened the .html file directly by double-clicking
   FIX    : NEVER open .html files directly!
            Always use: http://127.0.0.1:8000/
            The website MUST run through Python first

================================================================
  HOW TO RUN — STEP BY STEP
================================================================

STEP 1: Install Python (ONE TIME ONLY)
-----------------------------------------
  Download from: https://python.org/downloads/
  Install it. IMPORTANT: Check the box "Add Python to PATH"
  Then restart your PC or Command Prompt.

STEP 2: Double-click "INSTALL_AND_RUN.bat"
-----------------------------------------
  This will:
  - Install Django automatically
  - Set up the database
  - Load all 25 products
  - Start the website
  - Open your browser automatically

  That's it! You're done.

STEP 3: Every time after that
-----------------------------------------
  Just double-click "RUN_WEBSITE.bat"
  Website opens at: http://127.0.0.1:8000/

================================================================
  LOGIN DETAILS
================================================================

  Store   : http://127.0.0.1:8000/
  Admin   : http://127.0.0.1:8000/dashboard/login/
  Username: admin
  Password: mvsaqua2025

================================================================
  WHAT'S IN THIS WEBSITE
================================================================

  CUSTOMER SIDE:
  - Homepage with hero, categories, featured fish
  - Product listing with search and filter
  - Product detail pages with Add to Cart
  - Shopping cart with weight-based shipping (Rs.80/kg)
  - Checkout form (name, address, mobile)
  - WhatsApp order auto-message to +91 9490255775
  - Order tracking by Order ID (MVS10001 format)
  - PDF invoice download

  ADMIN PANEL (http://127.0.0.1:8000/dashboard/login/):
  - Dashboard with order stats and revenue
  - Add/Edit/Delete products with images
  - View and manage all orders
  - Change order status (Pending, Dispatched, Delivered)
  - Add tracking number and courier
  - Send WhatsApp confirmation and dispatch messages
  - Manage categories and customer reviews

  PRE-LOADED DATA:
  - 25 real products from your catalog
  - 6 categories (Fish, Equipment, Food, Plants, Medicine, Bowls)
  - 8 customer reviews
  - Admin account ready

================================================================
  PROJECT FILES
================================================================

  manage.py         - Django entry point (run this to start)
  seed_data.py      - Loads all products into database
  requirements.txt  - List of Python packages needed
  config/           - Django settings and URLs
  store/            - Products, categories, reviews app
  cart/             - Shopping cart app
  orders/           - Checkout, tracking, PDF invoice app
  dashboard/        - Admin panel app
  templates/        - All HTML page templates
  static/           - CSS and JS files
  media/            - Uploaded product images (add here)

================================================================
  ADDING PRODUCT IMAGES
================================================================

  1. Go to: http://127.0.0.1:8000/dashboard/login/
  2. Click "Products" in sidebar
  3. Click edit (pencil icon) on any product
  4. Upload image file
  5. Click Save

================================================================
  DEPLOY ONLINE (FREE - Render.com)
================================================================

  1. Create account at https://render.com
  2. Push this folder to GitHub
  3. New Web Service > Connect repo
  4. Build Command:
     pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate && python seed_data.py
  5. Start Command: gunicorn config.wsgi
  6. Done! Your website is live online.

================================================================

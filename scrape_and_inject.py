import urllib.request
import json
import re

url = "https://www.leichtbauwerkstatt.com/collections/all/products.json?limit=250"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
resp = urllib.request.urlopen(req)
data = json.loads(resp.read().decode('utf-8'))

products = data.get('products', [])

print(f"Loaded {len(products)} products from Shopify.")

html_cards = []
for i, p in enumerate(products):
    title = p.get('title', 'Unknown Part')
    desc_html = p.get('body_html', '')
    desc = re.sub('<[^<]+>', '', desc_html).strip()
    if len(desc) > 100: desc = desc[:100] + '...'
    elif not desc: desc = 'Precision engineered component.'
    
    category = p.get('product_type', 'Part')
    cat_lower = category.lower()
    
    variants = p.get('variants', [])
    price = 0
    vid = ''
    if variants:
        price = variants[0].get('price', '0')
        vid = str(variants[0].get('id', ''))
        
    images = p.get('images', [])
    img_url = 'https://images.unsplash.com/photo-1585386959984-a4155224a1ad?w=800&q=80'
    if images:
        src = images[0].get('src', '')
        if src: img_url = src
            
    card = f"""
            <div class="part-card bg-white dark:bg-zinc-950 p-0 reveal cursor-hover-target" data-category="{cat_lower}">
                <div class="overflow-hidden aspect-[4/3] bg-gray-100 dark:bg-zinc-900">
                    <img class="part-img w-full h-full object-cover grayscale hover:grayscale-0 transition-all duration-700"
                        src="{img_url}" loading="lazy" alt="{title}" onerror="this.src='https://images.unsplash.com/photo-1585386959984-a4155224a1ad?w=800&q=80'" />
                </div>
                <div class="p-6 space-y-4">
                    <div class="flex justify-between items-start">
                        <div class="pr-2">
                            <span class="badge text-[9px] uppercase tracking-[0.3em] text-neon-orange">{category} // 0{i+1}</span>
                            <h3 class="grotesk text-lg font-bold mt-1 text-gray-900 truncate" title="{title}">{title}</h3>
                            <p class="text-xs text-gray-500 mt-1 font-light leading-relaxed line-clamp-2">{desc}</p>
                        </div>
                        <span class="mono text-[10px] text-gray-400 bg-gray-50 dark:bg-zinc-900 px-2 py-1 border border-gray-200 dark:border-zinc-800 whitespace-nowrap">
                            In Stock
                        </span>
                    </div>
                    <div class="flex items-center justify-between pt-2 border-t border-gray-100 dark:border-zinc-800">
                        <div>
                            <p class="grotesk text-2xl font-bold text-gray-900">€{price}</p>
                            <p class="mono text-[9px] text-gray-400 uppercase">Per Unit</p>
                        </div>
                        <button
                            class="add-to-cart-btn bg-black dark:bg-white text-white dark:text-black px-6 py-3 text-[10px] uppercase tracking-widest font-bold hover:bg-neon-orange dark:hover:bg-neon-orange dark:hover:text-white transition-all duration-300 flex items-center gap-2"
                            data-id="{vid}" data-name="{title}" data-price="{price}" data-currency="EUR" data-img="{img_url}">
                            <span class="material-symbols-outlined text-sm">add</span>Add
                        </button>
                    </div>
                </div>
            </div>"""
    html_cards.append(card)

grid_html = f'<div id="parts-grid"\n            class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-px bg-gray-200 dark:bg-zinc-800 border border-gray-200 dark:border-zinc-800">\n' + ''.join(html_cards) + '\n        </div><!-- /parts-grid -->'

with open('parts.html', 'r') as f:
    html = f.read()

html = re.sub(r'<div id="parts-grid"[^>]*>.*?</div><!-- /parts-grid -->', grid_html, html, flags=re.DOTALL)

js_pattern = r'// ── Cart State ──.*?// ── Filters ──'
new_js = """// ── Cart State ──
        let cart = {};

        function formatPriceStr(amount, currency = 'EUR') { 
            return new Intl.NumberFormat('de-DE', { style: 'currency', currency }).format(amount); 
        }

        function updateCartUI() {
            const items = Object.values(cart);
            const count = items.reduce((s, i) => s + i.qty, 0);
            const total = items.reduce((s, i) => s + i.price * i.qty, 0);
            const countEl = document.getElementById('cart-count');
            countEl.textContent = count;
            count > 0 ? countEl.classList.remove('hidden') : countEl.classList.add('hidden');
            
            const currency = items.length > 0 ? items[0].currency : 'EUR';
            document.getElementById('cart-total').textContent = formatPriceStr(total, currency);

            const cartItemsEl = document.getElementById('cart-items');
            const emptyEl = document.getElementById('cart-empty');
            if (items.length === 0) { emptyEl.classList.remove('hidden'); cartItemsEl.innerHTML = ''; cartItemsEl.appendChild(emptyEl); return; }
            emptyEl.classList.add('hidden');
            cartItemsEl.innerHTML = items.map(item => `
            <div class="flex gap-4 items-start border-b border-gray-100 dark:border-zinc-800 pb-6" id="cart-item-${item.id}">
                <div class="w-20 h-20 bg-gray-100 dark:bg-zinc-800 flex-shrink-0 overflow-hidden">
                    <img src="${item.img || ''}" class="w-full h-full object-cover grayscale" onerror="this.style.display='none'"/>
                </div>
                <div class="flex-1 min-w-0">
                    <p class="grotesk font-semibold text-sm truncate" title="${item.name}">${item.name}</p>
                    <div class="flex items-center gap-3 mt-3">
                        <button class="qty-btn w-7 h-7 border border-gray-200 dark:border-zinc-700 text-sm font-bold flex items-center justify-center transition-all" onclick="changeQty('${item.id}', -1)">−</button>
                        <span class="mono text-sm font-bold w-4 text-center">${item.qty}</span>
                        <button class="qty-btn w-7 h-7 border border-gray-200 dark:border-zinc-700 text-sm font-bold flex items-center justify-center transition-all" onclick="changeQty('${item.id}', 1)">+</button>
                        <button class="ml-auto mono text-[9px] text-gray-400 hover:text-red-500 uppercase tracking-wider transition-colors" onclick="removeItem('${item.id}')">Remove</button>
                    </div>
                </div>
                <div class="text-right flex-shrink-0">
                    <p class="grotesk font-bold">${formatPriceStr(item.price * item.qty, item.currency)}</p>
                    <p class="mono text-[9px] text-gray-400">${formatPriceStr(item.price, item.currency)} ea.</p>
                </div>
            </div>
            `).join('');
        }

        window.changeQty = function(id, delta) {
            if (!cart[id]) return;
            cart[id].qty = Math.max(0, cart[id].qty + delta);
            if (cart[id].qty === 0) delete cart[id];
            updateCartUI();
        }

        window.removeItem = function(id) { delete cart[id]; updateCartUI(); }

        document.querySelectorAll('.add-to-cart-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const id = btn.dataset.id;
                if (cart[id]) { cart[id].qty++; } else {
                    cart[id] = { 
                        id, 
                        name: btn.dataset.name, 
                        price: parseFloat(btn.dataset.price), 
                        currency: btn.dataset.currency,
                        img: btn.dataset.img,
                        qty: 1 
                    };
                }
                updateCartUI();
                openCart();
                btn.textContent = '✓ Added';
                btn.classList.add('bg-neon-orange');
                setTimeout(() => { btn.innerHTML = '<span class="material-symbols-outlined text-sm">add</span>Add'; btn.classList.remove('bg-neon-orange'); }, 1200);
            });
        });

        // ── Cart Drawer ──
        const cartDrawer = document.getElementById('cart-drawer');
        const cartOverlay = document.getElementById('cart-overlay');
        function openCart() { cartDrawer.classList.add('open'); cartOverlay.classList.add('open'); document.body.style.overflow = 'hidden'; }
        function closeCart() { cartDrawer.classList.remove('open'); cartOverlay.classList.remove('open'); document.body.style.overflow = ''; }
        document.getElementById('cart-btn').addEventListener('click', openCart);
        document.getElementById('close-cart').addEventListener('click', closeCart);
        cartOverlay.addEventListener('click', closeCart);

        // ── Stripe Checkout ──
        const STRIPE_KEY = 'pk_test_REPLACE_WITH_YOUR_STRIPE_PUBLISHABLE_KEY';
        
        document.getElementById('checkout-btn').addEventListener('click', async () => {
            const items = Object.values(cart);
            if (items.length === 0) return;

            const btn = document.getElementById('checkout-btn');
            btn.innerHTML = '<span class="material-symbols-outlined text-sm animate-spin">progress_activity</span> Redirecting...';
            btn.disabled = true;

            const summary = items.map(i => `${i.name} ×${i.qty} — ${formatPriceStr(i.price * i.qty, i.currency)}`).join('\\n');
            const total = items.reduce((s, i) => s + i.price * i.qty, 0);
            
            // Dummy implementation of stripe until keys are provided
            if (STRIPE_KEY.includes('REPLACE')) {
                alert(`🔒 Stripe Integration Pending\\n\\nOrder Summary:\\n${summary}\\n\\nTotal: ${formatPriceStr(total, items[0].currency)}\\n\\nReplace STRIPE_KEY in parts.html to enable live checkout.`);
                btn.innerHTML = '<span>Proceed to Checkout</span><span class="material-symbols-outlined text-sm">arrow_forward</span>';
                btn.disabled = false;
                return;
            }

            try {
                const stripe = window.Stripe(STRIPE_KEY);
                // In a static setup without a backend, we usually redirect to a Stripe Payment Link 
                // Alternatively, you can list Price IDs manually.
            } catch (err) {
                console.error(err);
                btn.innerHTML = 'Error — Try Again';
                btn.disabled = false;
            }
        });

        // ── Filters ──"""

html = re.sub(js_pattern, new_js, html, flags=re.DOTALL)

if '<script src="https://js.stripe.com/v3/"></script>' not in html:
    html = html.replace('</head>', '    <script src="https://js.stripe.com/v3/"></script>\n</head>')

with open('parts.html', 'w') as f:
    f.write(html)

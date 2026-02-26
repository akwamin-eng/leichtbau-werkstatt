import re

with open('parts.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add Shopify Buy SDK to head
if 'shopify-buy' not in html:
    html = html.replace('</head>', '    <script src="https://sdks.shopifycdn.com/buy-button/latest/buy-button-storefront.min.js"></script>\n</head>')

# 2. Replace the static grid with an empty container and a loader
static_grid_regex = re.compile(r'<div id="parts-grid"[^>]*>.*?</div><!-- /parts-grid -->', re.DOTALL)

replacement_grid = """<div id="parts-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-px bg-gray-200 dark:bg-zinc-800 border border-gray-200 dark:border-zinc-800">
            <!-- Dynamic Shopify Products will load here -->
            <div id="parts-loader" class="col-span-full py-32 flex flex-col items-center justify-center text-gray-400">
                <span class="material-symbols-outlined text-4xl animate-spin mb-4">progress_activity</span>
                <p class="mono text-[10px] uppercase tracking-widest">Syncing Live Inventory...</p>
            </div>
        </div><!-- /parts-grid -->"""

html = static_grid_regex.sub(replacement_grid, html)

# 3. Replace the static Javascript with the dynamic Shopify script
static_js_regex = re.compile(r'// ── Cart State ──.*?// ── Dark Mode Persistence ──', re.DOTALL)

dynamic_js = """// ── Shopify Storefront API Integration ──
        const client = ShopifyBuy.buildClient({
            domain: 'leichtbau-werkstatt.myshopify.com',
            storefrontAccessToken: 'e5e8a5b292e7c3b999c0ac7b3d3ab2c6' // Public unauthenticated storefront API token
        });

        let cartId = localStorage.getItem('shopify_cart_id');
        let checkout;

        async function initShopify() {
            // 1. Initialize or fetch Checkout (Cart)
            if (cartId) {
                checkout = await client.checkout.fetch(cartId);
                // If the checkout was completed, create a new one
                if (checkout && checkout.completedAt) {
                    checkout = await client.checkout.create();
                    localStorage.setItem('shopify_cart_id', checkout.id);
                }
            } else {
                checkout = await client.checkout.create();
                localStorage.setItem('shopify_cart_id', checkout.id);
            }
            updateCartUI();

            // 2. Fetch Products
            const products = await client.product.fetchAll();
            renderProducts(products);
            
            // 3. Bind Checkout Button
            document.getElementById('checkout-btn').addEventListener('click', () => {
                if(checkout.lineItems.length > 0) {
                    window.location.href = checkout.webUrl;
                }
            });
        }

        function formatPriceStr(amount, currency = 'EUR') {
            return new Intl.NumberFormat('de-DE', { style: 'currency', currency }).format(amount);
        }

        function renderProducts(products) {
            const grid = document.getElementById('parts-grid');
            grid.innerHTML = ''; // Clear loader
            
            if (products.length === 0) {
                grid.innerHTML = `<div class="col-span-full py-20 text-center text-gray-500 mono text-xs uppercase">No products available at the moment.</div>`;
                return;
            }

            products.forEach((product, i) => {
                const variant = product.variants[0];
                const price = variant.price.amount;
                const src = product.images.length > 0 ? product.images[0].src : 'https://images.unsplash.com/photo-1585386959984-a4155224a1ad?w=800&q=80';
                
                // Determine category from tags or product type for the filter
                let category = product.productType ? product.productType.toLowerCase() : 'custom';
                
                const card = document.createElement('div');
                card.className = "part-card bg-white dark:bg-zinc-950 p-0 reveal cursor-hover-target shown";
                card.dataset.category = category;
                card.innerHTML = `
                <div class="overflow-hidden aspect-[4/3] bg-gray-100 dark:bg-zinc-900 relative">
                    <img class="part-img w-full h-full object-cover grayscale hover:grayscale-0 transition-all duration-700"
                        src="${src}" loading="lazy" alt="${product.title}" />
                    ${!product.availableForSale ? `<div class="absolute inset-0 bg-black/60 flex items-center justify-center"><span class="bg-neon-orange text-white text-[10px] font-bold uppercase tracking-widest px-3 py-1">Sold Out</span></div>` : ''}
                </div>
                <div class="p-6 space-y-4">
                    <div class="flex justify-between items-start">
                        <div class="pr-2">
                            <span class="badge text-[9px] uppercase tracking-[0.3em] text-neon-orange">${category} // 0${i+1}</span>
                            <h3 class="grotesk text-lg font-bold mt-1 text-gray-900 truncate" title="${product.title}">${product.title}</h3>
                            <p class="text-xs text-gray-500 mt-1 font-light leading-relaxed line-clamp-2">${product.description || 'Premium aftermarket component.'}</p>
                        </div>
                        ${product.availableForSale ? `
                        <span class="mono text-[10px] text-gray-400 bg-gray-50 dark:bg-zinc-900 px-2 py-1 border border-gray-200 dark:border-zinc-800 whitespace-nowrap">
                            In Stock
                        </span>` : ''}
                    </div>
                    <div class="flex items-center justify-between pt-2 border-t border-gray-100 dark:border-zinc-800">
                        <div>
                            <p class="grotesk text-2xl font-bold text-gray-900">€${price}</p>
                            <p class="mono text-[9px] text-gray-400 uppercase">Per Unit</p>
                        </div>
                        <button
                            class="add-to-cart-btn bg-black dark:bg-white text-white dark:text-black px-6 py-3 text-[10px] uppercase tracking-widest font-bold hover:bg-neon-orange dark:hover:bg-neon-orange dark:hover:text-white transition-all duration-300 flex items-center gap-2 ${!product.availableForSale ? 'opacity-50 cursor-not-allowed' : ''}"
                            data-variant-id="${variant.id}" ${!product.availableForSale ? 'disabled' : ''}>
                            <span class="material-symbols-outlined text-sm">add</span>Add
                        </button>
                    </div>
                </div>`;
                grid.appendChild(card);
            });

            // Bind add to cart events for the newly rendered buttons
            document.querySelectorAll('.add-to-cart-btn').forEach(btn => {
                btn.addEventListener('click', async (e) => {
                    const ogHtml = btn.innerHTML;
                    btn.innerHTML = '<span class="material-symbols-outlined text-sm animate-spin">progress_activity</span> Syncing';
                    btn.disabled = true;
                    
                    const variantId = btn.dataset.variantId;
                    const lineItemsToAdd = [{ variantId, quantity: 1 }];
                    
                    try {
                        checkout = await client.checkout.addLineItems(checkout.id, lineItemsToAdd);
                        updateCartUI();
                        openCart();
                        
                        btn.innerHTML = '✓ Added';
                        btn.classList.add('bg-neon-orange');
                        btn.classList.remove('bg-black', 'dark:bg-white');
                        setTimeout(() => { 
                            btn.innerHTML = ogHtml; 
                            btn.classList.remove('bg-neon-orange'); 
                            btn.classList.add('bg-black', 'dark:bg-white');
                            btn.disabled = false;
                        }, 1200);
                    } catch(err) {
                        console.error(err);
                        btn.innerHTML = 'Error';
                        setTimeout(() => { btn.innerHTML = ogHtml; btn.disabled = false; }, 2000);
                    }
                });
            });
        }

        function updateCartUI() {
            const countEl = document.getElementById('cart-count');
            const totalItems = checkout.lineItems.reduce((acc, item) => acc + item.quantity, 0);
            
            countEl.textContent = totalItems;
            totalItems > 0 ? countEl.classList.remove('hidden') : countEl.classList.add('hidden');
            
            document.getElementById('cart-total').textContent = formatPriceStr(checkout.totalPrice.amount, checkout.totalPrice.currencyCode);

            const cartItemsEl = document.getElementById('cart-items');
            const emptyEl = document.getElementById('cart-empty');
            
            if (checkout.lineItems.length === 0) { 
                emptyEl.classList.remove('hidden'); 
                cartItemsEl.innerHTML = ''; 
                cartItemsEl.appendChild(emptyEl); 
                return; 
            }
            
            emptyEl.classList.add('hidden');
            cartItemsEl.innerHTML = checkout.lineItems.map(item => `
            <div class="flex gap-4 items-start border-b border-gray-100 dark:border-zinc-800 pb-6">
                <div class="w-20 h-20 bg-gray-100 dark:bg-zinc-800 flex-shrink-0 overflow-hidden">
                    <img src="${item.variant.image ? item.variant.image.src : ''}" class="w-full h-full object-cover grayscale" onerror="this.style.display='none'"/>
                </div>
                <div class="flex-1 min-w-0">
                    <p class="grotesk font-semibold text-sm truncate" title="${item.title}">${item.title}</p>
                    <div class="flex items-center gap-3 mt-3">
                        <button class="qty-btn w-7 h-7 border border-gray-200 dark:border-zinc-700 text-sm font-bold flex items-center justify-center transition-all" onclick="updateLineItem('${item.id}', ${item.quantity - 1})">−</button>
                        <span class="mono text-sm font-bold w-4 text-center">${item.quantity}</span>
                        <button class="qty-btn w-7 h-7 border border-gray-200 dark:border-zinc-700 text-sm font-bold flex items-center justify-center transition-all" onclick="updateLineItem('${item.id}', ${item.quantity + 1})">+</button>
                        <button class="ml-auto mono text-[9px] text-gray-400 hover:text-red-500 uppercase tracking-wider transition-colors" onclick="removeLineItem('${item.id}')">Remove</button>
                    </div>
                </div>
                <div class="text-right flex-shrink-0">
                    <p class="grotesk font-bold">${formatPriceStr(item.variant.price.amount * item.quantity, item.variant.price.currencyCode)}</p>
                    <p class="mono text-[9px] text-gray-400">${formatPriceStr(item.variant.price.amount, item.variant.price.currencyCode)} ea.</p>
                </div>
            </div>
            `).join('');
        }

        window.updateLineItem = async function(id, quantity) {
            if(quantity === 0) {
                return removeLineItem(id);
            }
            try {
                checkout = await client.checkout.updateLineItems(checkout.id, [{id, quantity}]);
                updateCartUI();
            } catch(e) { console.error(e); }
        }

        window.removeLineItem = async function(id) {
            try {
                checkout = await client.checkout.removeLineItems(checkout.id, [id]);
                updateCartUI();
            } catch(e) { console.error(e); }
        }

        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                const filter = btn.dataset.filter;
                document.querySelectorAll('.part-card').forEach(card => {
                    // Match subset of string for custom loose categories
                    const match = filter === 'all' || card.dataset.category.includes(filter);
                    card.style.display = match ? '' : 'none';
                });
            });
        });

        // Initialize wrapper
        initShopify();

        // ── Cart Drawer Events ──
        const cartDrawer = document.getElementById('cart-drawer');
        const cartOverlay = document.getElementById('cart-overlay');
        function openCart() { cartDrawer.classList.add('open'); cartOverlay.classList.add('open'); document.body.style.overflow = 'hidden'; }
        function closeCart() { cartDrawer.classList.remove('open'); cartOverlay.classList.remove('open'); document.body.style.overflow = ''; }
        document.getElementById('cart-btn').addEventListener('click', openCart);
        document.getElementById('close-cart').addEventListener('click', closeCart);
        cartOverlay.addEventListener('click', closeCart);

        // ── Dark Mode Persistence ──"""

html = static_js_regex.sub(dynamic_js, html)

with open('parts.html', 'w', encoding='utf-8') as f:
    f.write(html)

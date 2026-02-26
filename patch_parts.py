import re

with open('parts.html', 'r') as f:
    html = f.read()

# Remove static parts grid
html = re.sub(
    r'<div id="parts-grid"[^>]*>.*?</div><!-- /parts-grid -->',
    r'<div id="parts-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-px bg-gray-200 dark:bg-zinc-800 border border-gray-200 dark:border-zinc-800"><div class="p-12 text-center col-span-full"><p class="mono text-xs uppercase tracking-widest text-gray-500 animate-pulse">Loading Live Inventory from Shopify...</p></div></div><!-- /parts-grid -->',
    html,
    flags=re.DOTALL
)

# Remove Stripe script
html = re.sub(r'<script src="https://js\.stripe\.com/v3/"></script>\s*', '', html)

# Replace Javascript
js_code = """
    <script>
        // ── Cursor ──
        const cursor = document.getElementById('cursor');
        document.addEventListener('mousemove', e => { cursor.style.left = e.clientX + 'px'; cursor.style.top = e.clientY + 'px'; });
        const initCursor = () => {
            document.querySelectorAll('.cursor-hover-target').forEach(el => {
                el.addEventListener('mouseenter', () => cursor.classList.add('hovered'));
                el.addEventListener('mouseleave', () => cursor.classList.remove('hovered'));
            });
        };
        initCursor();

        // ── Reveal on Scroll ──
        const initReveals = () => {
            const reveals = document.querySelectorAll('.reveal');
            const observer = new IntersectionObserver(entries => {
                entries.forEach((e, i) => { if (e.isIntersecting) { setTimeout(() => e.target.classList.add('shown'), i * 60); observer.unobserve(e.target); } });
            }, { threshold: 0.08 });
            reveals.forEach(el => observer.observe(el));
        };
        initReveals();

        // ── SHOPIFY INTEGRATION ──
        const domain = 'leichtbauwerkstatt.myshopify.com';
        const storefrontAccessToken = '926696394506a6845f32593799e52fa1';
        const apiVersion = '2024-01';

        async function shopifyFetch(query, variables = {}) {
            const res = await fetch(`https://${domain}/api/${apiVersion}/graphql.json`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Shopify-Storefront-Access-Token': storefrontAccessToken
                },
                body: JSON.stringify({ query, variables })
            });
            return res.json();
        }

        // Fetch Products
        async function loadProducts() {
            const query = `
            {
              products(first: 20) {
                edges {
                  node {
                    id
                    title
                    handle
                    description
                    productType
                    variants(first: 1) {
                      edges {
                        node {
                          id
                          price {
                            amount
                            currencyCode
                          }
                          quantityAvailable
                        }
                      }
                    }
                    images(first: 1) {
                      edges {
                        node {
                          url(transform: {maxWidth: 800, maxHeight: 600, crop: CENTER})
                          altText
                        }
                      }
                    }
                  }
                }
              }
            }`;

            try {
                const { data } = await shopifyFetch(query);
                renderProducts(data.products.edges);
            } catch (err) {
                console.error("Error fetching from Shopify", err);
                document.getElementById('parts-grid').innerHTML = '<div class="p-12 text-center col-span-full"><p class="mono text-xs uppercase text-red-500">Failed to load inventory.</p></div>';
            }
        }

        function renderProducts(edges) {
            const grid = document.getElementById('parts-grid');
            if (!edges || edges.length === 0) {
                grid.innerHTML = '<div class="p-12 text-center col-span-full"><p class="mono text-xs uppercase tracking-widest text-gray-500">No products found in store.</p></div>';
                return;
            }

            const html = edges.map((edge, index) => {
                const p = edge.node;
                const variant = p.variants.edges[0]?.node;
                const price = variant?.price?.amount ? parseFloat(variant.price.amount) : 0;
                const currency = variant?.price?.currencyCode || 'EUR';
                const vId = variant?.id || '';
                
                const imgUrl = p.images.edges[0]?.node?.url || 'https://images.unsplash.com/photo-1585386959984-a4155224a1ad?w=800&q=80';
                const type = p.productType || 'Part';
                const formattedPrice = new Intl.NumberFormat('de-DE', { style: 'currency', currency }).format(price);

                return `
                <div class="part-card bg-white dark:bg-zinc-950 p-0 reveal cursor-hover-target" data-category="${type.toLowerCase()}">
                    <div class="overflow-hidden aspect-[4/3] bg-gray-100 dark:bg-zinc-900">
                        <img class="part-img w-full h-full object-cover grayscale hover:grayscale-0 transition-all duration-700"
                            src="${imgUrl}" alt="${p.title}" loading="lazy" />
                    </div>
                    <div class="p-6 space-y-4">
                        <div class="flex justify-between items-start">
                            <div class="pr-2">
                                <span class="badge text-[9px] uppercase tracking-[0.3em] text-neon-orange">${type} // 0${index + 1}</span>
                                <h3 class="grotesk text-lg font-bold mt-1 text-gray-900 truncate" title="${p.title}">${p.title}</h3>
                                <p class="text-xs text-gray-500 mt-1 font-light leading-relaxed line-clamp-2">${p.description || 'Precision engineered component.'}</p>
                            </div>
                            <span class="mono text-[10px] text-gray-400 bg-gray-50 dark:bg-zinc-900 px-2 py-1 border border-gray-200 dark:border-zinc-800 whitespace-nowrap">
                                In Stock
                            </span>
                        </div>
                        <div class="flex items-center justify-between pt-2 border-t border-gray-100 dark:border-zinc-800">
                            <div>
                                <p class="grotesk text-2xl font-bold text-gray-900">${formattedPrice}</p>
                                <p class="mono text-[9px] text-gray-400 uppercase">Per Unit</p>
                            </div>
                            <button
                                class="add-to-cart-btn bg-black dark:bg-white text-white dark:text-black px-6 py-3 text-[10px] uppercase tracking-widest font-bold hover:bg-neon-orange dark:hover:bg-neon-orange dark:hover:text-white transition-all duration-300 flex items-center gap-2"
                                data-id="${vId}" data-name="${p.title}" data-price="${price}" data-currency="${currency}" data-img="${imgUrl}">
                                <span class="material-symbols-outlined text-sm">add</span>Add
                            </button>
                        </div>
                    </div>
                </div>`;
            }).join('');

            grid.innerHTML = html;
            initCursor();
            initReveals();
            attachCartListeners();
        }

        // ── Cart State ──
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
            
            // Assume single currency for display simplicity
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

        function attachCartListeners() {
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
        }

        // ── Cart Drawer ──
        const cartDrawer = document.getElementById('cart-drawer');
        const cartOverlay = document.getElementById('cart-overlay');
        function openCart() { cartDrawer.classList.add('open'); cartOverlay.classList.add('open'); document.body.style.overflow = 'hidden'; }
        function closeCart() { cartDrawer.classList.remove('open'); cartOverlay.classList.remove('open'); document.body.style.overflow = ''; }
        document.getElementById('cart-btn').addEventListener('click', openCart);
        document.getElementById('close-cart').addEventListener('click', closeCart);
        cartOverlay.addEventListener('click', closeCart);

        // ── Shopify Checkout ──
        document.getElementById('checkout-btn').addEventListener('click', async () => {
            const items = Object.values(cart);
            if (items.length === 0) return;

            const btn = document.getElementById('checkout-btn');
            btn.innerHTML = '<span class="material-symbols-outlined text-sm animate-spin">progress_activity</span> Redirecting...';
            btn.disabled = true;

            const lines = items.map(item => ({
                merchandiseId: item.id,
                quantity: item.qty
            }));

            const query = `
            mutation cartCreate($input: CartInput!) {
              cartCreate(input: $input) {
                cart {
                  checkoutUrl
                }
                userErrors {
                  field
                  message
                }
              }
            }`;

            try {
                const { data } = await shopifyFetch(query, { input: { lines } });
                if (data.cartCreate.cart.checkoutUrl) {
                    window.location.href = data.cartCreate.cart.checkoutUrl;
                } else {
                    console.error("Checkout errors", data.cartCreate.userErrors);
                    alert("Unable to create checkout. Try again.");
                    btn.innerHTML = '<span>Proceed to Checkout</span><span class="material-symbols-outlined text-sm">arrow_forward</span>';
                    btn.disabled = false;
                }
            } catch (err) {
                console.error(err);
                btn.innerHTML = 'Error — Try Again';
                btn.disabled = false;
            }
        });

        // ── Filters ──
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                const filter = btn.dataset.filter.toLowerCase();
                document.querySelectorAll('.part-card').forEach(card => {
                    // Match category if available, otherwise just show all unless strict filtering is needed
                    // Because Shopify product types might not strictly match our tabs, we'll do a loose text match
                    const productText = card.innerText.toLowerCase();
                    const match = filter === 'all' || card.dataset.category.includes(filter) || productText.includes(filter);
                    card.style.display = match ? '' : 'none';
                });
            });
        });

        // ── Init ──
        if (localStorage.getItem('asta-theme') === 'dark') document.documentElement.classList.add('dark');
        loadProducts();
    </script>"""

# Replace script tag and everything down to bottom
html = re.sub(r'<script>\s*// ── Cursor ──.*?</script>', js_code, html, flags=re.DOTALL)

with open('parts.html', 'w') as f:
    f.write(html)

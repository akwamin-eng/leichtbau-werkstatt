with open("index.html", "r") as f:
    idx = f.read()

index_instagram = """                        <a class="group flex items-center space-x-2 cursor-hover-target" href="#">
                            <span
                                class="w-2 h-2 bg-black dark:bg-white rounded-full group-hover:bg-neon-orange transition-colors"></span>
                            <span class="text-xs font-bold uppercase tracking-widest dark:text-white">Instagram</span>
                        </a>"""

index_yelp = """                        <a class="group flex items-center space-x-2 cursor-hover-target" href="https://www.yelp.com/biz/leichtbau-costa-mesa?osq=leichtbau" target="_blank" rel="noopener">
                            <span
                                class="w-2 h-2 bg-black dark:bg-white rounded-full group-hover:bg-neon-orange transition-colors"></span>
                            <span class="text-xs font-bold uppercase tracking-widest dark:text-white flex items-center gap-1">Yelp <span class="text-neon-orange tracking-tighter text-[10px] mt-[1px]">★★★★★</span></span>
                        </a>"""

idx = idx.replace(index_instagram, index_yelp + "\n" + index_instagram)

with open("index.html", "w") as f:
    f.write(idx)

with open("contact.html", "r") as f:
    cnt = f.read()

contact_instagram = """                        <a class="group flex items-center space-x-2" href="#">
                            <span
                                class="w-1.5 h-1.5 bg-black dark:bg-white rounded-full group-hover:bg-neon-orange transition-colors"></span>
                            <span
                                class="text-xs font-bold uppercase tracking-widest group-hover:text-neon-orange transition-colors">Instagram</span>
                        </a>"""

contact_yelp = """                        <a class="group flex items-center space-x-2" href="https://www.yelp.com/biz/leichtbau-costa-mesa?osq=leichtbau" target="_blank" rel="noopener">
                            <span
                                class="w-1.5 h-1.5 bg-black dark:bg-white rounded-full group-hover:bg-neon-orange transition-colors"></span>
                            <span
                                class="text-xs font-bold uppercase tracking-widest group-hover:text-neon-orange transition-colors flex items-center gap-1">Yelp <span class="text-neon-orange tracking-tighter text-[10px] mt-[1px]">★★★★★</span></span>
                        </a>"""

cnt = cnt.replace(contact_instagram, contact_yelp + "\n" + contact_instagram)

with open("contact.html", "w") as f:
    f.write(cnt)


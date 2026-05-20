document.addEventListener('DOMContentLoaded', () => {
    // 0. Glass Navbar Scroll Effect
    const navbar = document.getElementById('navbar');
    if (navbar) {
        const onScroll = () => {
            const isAlwaysScrolled = navbar.classList.contains('always-scrolled') || 
                (navbar.classList.contains('always-scrolled-light') && !document.documentElement.classList.contains('dark'));
            
            if (isAlwaysScrolled || window.scrollY > 40) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        };
        window.addEventListener('scroll', onScroll, { passive: true });
        onScroll(); // Run once on load in case page is already scrolled
    }

    // 0.1 Active Nav Link Highlighting
    const highlightActiveNav = () => {
        const currentPath = window.location.pathname.split('/').pop() || 'index.html';
        const navLinks = document.querySelectorAll('#navbar nav a');
        
        // Home pages list
        const homePages = ['index.html', 'home2.html', ''];

        navLinks.forEach(link => {
            const href = link.getAttribute('href');
            let isActive = false;

            if (href === currentPath) {
                isActive = true;
            } else if (homePages.includes(currentPath) && href === 'index.html' && link.classList.contains('nav-home')) {
                // Special case for Home parent link when on any home page
                isActive = true;
            }

            if (isActive) {
                link.classList.add('active');
                link.classList.add('text-primary');
                
                // If it's a dropdown child, also highlight the trigger
                const dropdown = link.closest('.nav-dropdown');
                if (dropdown) {
                    const trigger = dropdown.parentElement.querySelector('.dropdown-trigger');
                    if (trigger) {
                        trigger.classList.add('active');
                        trigger.classList.add('text-primary');
                    }
                }
            } else {
                // Only remove if it's not already handled as a parent trigger
                if (!link.classList.contains('dropdown-trigger')) {
                    link.classList.remove('active');
                    link.classList.remove('text-primary');
                }
            }
        });
    };
    highlightActiveNav();


    const html = document.documentElement;
    const themeToggles = document.querySelectorAll('[id^="theme-toggle"]');
    const dirToggles = document.querySelectorAll('[id^="dir-toggle"]');

    // Theme Logic
    const currentTheme = localStorage.getItem('theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    if (currentTheme === 'dark') {
        html.classList.add('dark');
    } else {
        html.classList.remove('dark');
        html.classList.add('light');
    }

    const updateThemeIcons = () => {
        const isDark = html.classList.contains('dark');
        themeToggles.forEach(btn => {
            const darkIcon = btn.querySelector('.hidden.dark\\:block');
            const lightIcon = btn.querySelector('.dark\\:hidden');
            if (isDark) {
                if (darkIcon) darkIcon.style.display = 'block';
                if (lightIcon) lightIcon.style.display = 'none';
            } else {
                if (darkIcon) darkIcon.style.display = 'none';
                if (lightIcon) lightIcon.style.display = 'block';
            }
        });
    };

    themeToggles.forEach(toggle => {
        toggle.addEventListener('click', () => {
            if (html.classList.contains('dark')) {
                html.classList.remove('dark');
                html.classList.add('light');
                localStorage.setItem('theme', 'light');
            } else {
                html.classList.add('dark');
                html.classList.remove('light');
                localStorage.setItem('theme', 'dark');
            }
            updateThemeIcons();
            window.dispatchEvent(new Event('scroll'));
        });
    });

    // Direction Logic
    const updateDirUI = (dir) => {
        html.setAttribute('dir', dir);
        localStorage.setItem('dir', dir);
        dirToggles.forEach(btn => {
            // Always show the TARGET direction as the button label
            btn.textContent = dir === 'ltr' ? 'RTL' : 'LTR';
        });
    };

    const currentDir = localStorage.getItem('dir') || 'ltr';
    updateDirUI(currentDir);

    dirToggles.forEach(toggle => {
        toggle.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Disable transitions temporarily to prevent sweep animations
            html.classList.add('disable-transitions');
            
            const newDir = html.getAttribute('dir') === 'ltr' ? 'rtl' : 'ltr';
            updateDirUI(newDir);
            
            // Force reflow and re-enable transitions
            setTimeout(() => {
                html.classList.remove('disable-transitions');
            }, 50);
        });
    });

    // 2. Global Hover Effects for Cards
    // Select any container that looks like a card based on typical Tailwind class names used in these templates
    const possibleCards = document.querySelectorAll(
        '.group, [class*="rounded-none"], [class*="rounded-xl"], article'
    );

    possibleCards.forEach(card => {
        // Verify it's not a button or input to avoid breaking interactive elements
        if (card.tagName.toLowerCase() === 'button' || card.tagName.toLowerCase() === 'input' || card.tagName.toLowerCase() === 'a') return;
        
        // Often cards have extensive padding or images
        const hasBackground = card.className.includes('bg-') || card.className.includes('border');
        if (!hasBackground) return;

        // Apply transition styling for the card uplift
        card.style.transition = 'transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.4s ease';
        
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-10px)';
            card.style.boxShadow = '0 25px 50px -12px rgba(0, 0, 0, 0.25)';
            
            // Find images and zoom them
            const images = card.querySelectorAll('img, [style*="background-image"]');
            images.forEach(img => {
                // Determine if it's the main parent for an image cover
                if(img.style) {
                    img.style.transition = 'transform 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
                    img.style.transform = 'scale(1.1)';
                }
            });
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0)';
            card.style.boxShadow = '';
            
            // Restore image zoom
            const images = card.querySelectorAll('img, [style*="background-image"]');
            images.forEach(img => {
                if(img.style) {
                    img.style.transform = 'scale(1)';
                }
            });
        });
    });

    // 3. Dropdowns handled by CSS (hover)

    // 4. Mobile Menu Drawer Logic
    const mobileMenuTrigger = document.getElementById('mobile-menu-trigger');
    const mobileMenuClose = document.getElementById('mobile-menu-close');
    const mobileDrawer = document.getElementById('mobile-drawer');
    const drawerOverlay = document.getElementById('drawer-overlay');

    const openDrawer = () => {
        mobileDrawer.classList.remove('translate-x-full');
        mobileDrawer.classList.add('translate-x-0');
        drawerOverlay.classList.remove('opacity-0', 'invisible');
        drawerOverlay.classList.add('opacity-100', 'visible');
        document.body.style.overflow = 'hidden'; // Prevent scrolling when menu is open
    };

    const closeDrawer = () => {
        mobileDrawer.classList.add('translate-x-full');
        mobileDrawer.classList.remove('translate-x-0');
        drawerOverlay.classList.add('opacity-0', 'invisible');
        drawerOverlay.classList.remove('opacity-100', 'visible');
        document.body.style.overflow = '';
    };

    if (mobileMenuTrigger) {
        mobileMenuTrigger.addEventListener('click', openDrawer);
    }

    if (mobileMenuClose) {
        mobileMenuClose.addEventListener('click', (e) => {
            e.stopPropagation();
            closeDrawer();
        });
    }

    if (drawerOverlay) {
        drawerOverlay.addEventListener('click', closeDrawer);
    }

    // 3.1 Mobile Drawer Accordion Toggle
    const accordionTriggers = document.querySelectorAll('.drawer-accordion-trigger');
    accordionTriggers.forEach(trigger => {
        trigger.addEventListener('click', () => {
            const content = trigger.nextElementSibling;
            const icon = trigger.querySelector('.accordion-icon');
            
            if (content) {
                content.classList.toggle('hidden');
                if (icon) {
                    icon.style.transform = content.classList.contains('hidden') ? 'rotate(0deg)' : 'rotate(180deg)';
                }
            }
        });
    });

    // Close drawer on escape key
    window.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeDrawer();
    });

    // 5. Coming Soon Floating Button Injection
    

    // 6. Global Form Validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            let isValid = true;
            const submitBtn = form.querySelector('button[type="submit"]');

            // Reset previous visual errors
            form.querySelectorAll('.border-red-500').forEach(el => {
                el.classList.remove('border-red-500', 'ring-red-500', 'ring-1', '!border-red-500');
            });
            form.querySelectorAll('.text-red-500').forEach(el => {
                if(el.tagName === 'SPAN' && el.classList.contains('absolute')) {
                     el.classList.remove('text-red-500');
                }
            });

            // Find all inputs (exclude hidden/checkboxes)
            const inputs = form.querySelectorAll('input:not([type="hidden"]):not([type="checkbox"]), textarea, select');
            
            inputs.forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                    showError(input);
                }
                
                if (input.type === 'email' && input.value.trim()) {
                    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                    if (!emailRegex.test(input.value)) {
                        isValid = false;
                        showError(input);
                    }
                }
            });

            if (isValid && submitBtn) {
                const originalText = submitBtn.innerHTML;
                submitBtn.classList.add('bg-emerald-500', '!text-white', 'border-emerald-500');
                submitBtn.classList.remove('bg-primary', 'bg-blue-600');
                submitBtn.innerHTML = '<span class="material-symbols-outlined text-[18px]">check_circle</span> Validating...';
                
                setTimeout(() => {
                    submitBtn.innerHTML = '<span class="material-symbols-outlined text-[18px]">verified</span> Success';
                    setTimeout(() => {
                        submitBtn.classList.remove('bg-emerald-500', '!text-white', 'border-emerald-500');
                        submitBtn.classList.add(submitBtn.hasAttribute('data-original-bg') ? submitBtn.getAttribute('data-original-bg') : 'bg-primary');
                        submitBtn.innerHTML = originalText;
                        if (!form.classList.contains('no-reset')) form.reset();
                    }, 2000);
                }, 1000);
            }
        });
    });

    function showError(input) {
        input.classList.add('border-red-500', 'ring-red-500', 'ring-1', '!border-red-500', 'transition-all');
        const parent = input.parentElement;
        if(parent.classList.contains('relative')){
             const icon = parent.querySelector('span.absolute');
             if(icon) icon.classList.add('text-red-500');
        }
    }

    // 7. Inline Subscription Success Handler
    const showInlineSuccess = (container, message) => {
        // Remove existing success message if any
        const existing = container.parentElement.querySelector('.subscription-success-text');
        if (existing) existing.remove();

        const successMsg = document.createElement('div');
        successMsg.className = 'subscription-success-text';
        successMsg.textContent = message;
        container.parentElement.appendChild(successMsg);

        // Trigger animation
        setTimeout(() => successMsg.classList.add('active'), 10);

        // Remove after 5 seconds
        setTimeout(() => {
            successMsg.classList.remove('active');
            setTimeout(() => successMsg.remove(), 500);
        }, 5000);
    };

    // Footer Subscribe Handler
    const allFooterButtons = document.querySelectorAll('footer button');
    let subBtn = null;
    let subInput = null;

    allFooterButtons.forEach(btn => {
        const icon = btn.querySelector('.material-symbols-outlined');
        if (icon && (icon.textContent.trim() === 'send' || icon.innerText.trim() === 'send')) {
            subBtn = btn;
            subInput = btn.parentElement.querySelector('input[type="email"]');
        }
    });

    // Fallback: search by heading if not found by icon
    if (!subBtn || !subInput) {
        const footerHeadings = Array.from(document.querySelectorAll('footer h4, footer h5'));
        const subscribeHeading = footerHeadings.find(h => h.textContent.toLowerCase().includes('subscribe'));
        if (subscribeHeading) {
            const container = subscribeHeading.parentElement;
            subBtn = subBtn || container.querySelector('button');
            subInput = subInput || container.querySelector('input[type="email"]');
        }
    }

    if (subBtn && subInput) {
        const subscribeContainer = subBtn.parentElement; // The flex container

        subBtn.addEventListener('click', () => {
            const email = subInput.value.trim();
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            
            if (emailRegex.test(email)) {
                showInlineSuccess(subscribeContainer, "Thanks for choosing us");
                subInput.value = '';
                subInput.classList.remove('border-red-500', 'ring-1', 'ring-red-500');
            } else {
                subInput.classList.add('border-red-500', 'ring-1', 'ring-red-500');
                subInput.focus();
            }
        });
        
        // Allow entry key
        subInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') subBtn.click();
        });
    }
    window.currentDate = new Date();
    
    // Sample Events with full card data
    const calendarEvents = [
        { 
            date: new Date(2025, 5, 27), 
            title: "Mountain Portrait Session", 
            title2: "Elite Wedding & Commercial Shoot", 
            type: "premium", 
            time: "09:00 AM - 02:00 PM",
            photographer: "Alex Lumini",
            detailerImg: "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?q=80&w=1974&auto=format&fit=crop",
            status: "Confirmed",
            image: "https://images.unsplash.com/photo-1493863641943-9b68992a8d07?q=80&w=2058&auto=format&fit=crop"
        },
        { 
            date: new Date(2025, 6, 15), 
            title: "Coastal Wedding Shoot", 
            title2: "Advanced Retouching & Color Grading", 
            type: "maintenance", 
            time: "10:00 AM - 04:00 PM",
            photographer: "Sarah Lens",
            detailerImg: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?q=80&w=1974&auto=format&fit=crop",
            status: "Pending",
            image: "https://images.unsplash.com/photo-1544005313-94ddf0286df2?q=80&w=1976&auto=format&fit=crop"
        },
        { 
            date: new Date(2025, 6, 21), 
            title: "Urban Lifestyle Shoot", 
            title2: "Deep Portfolio Review", 
            type: "interior", 
            time: "08:30 AM - 12:30 PM",
            photographer: "David Snap",
            detailerImg: "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?q=80&w=2070&auto=format&fit=crop",
            status: "Confirmed",
            image: "https://images.unsplash.com/photo-1523275335684-37898b6baf30?q=80&w=1999&auto=format&fit=crop"
        },
        { 
            date: new Date(2025, 7, 5), 
            title: "Product Branding Session", 
            title2: "Advanced Product Editing", 
            type: "premium", 
            time: "08:00 AM - 05:00 PM",
            photographer: "Alex Lumini",
            detailerImg: "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?q=80&w=1974&auto=format&fit=crop",
            status: "Confirmed",
            image: "https://images.unsplash.com/photo-1542038784456-1ea8e935640e?q=80&w=2070&auto=format&fit=crop"
        }
    ];

    window.renderUpcomingAppointments = function() {
        const container = document.getElementById('upcoming-appointments-list');
        if (!container) return;

        container.innerHTML = '';
        
        // Sort by date (nearest first)
        const sortedEvents = [...calendarEvents].sort((a, b) => a.date - b.date);

        sortedEvents.forEach(event => {
            const dateStr = event.date.toLocaleDateString('en-US', { month: 'short', day: '2-digit', year: 'numeric' });
            const statusClass = event.status === 'Confirmed' ? 'bg-emerald-500/10 text-emerald-500 border-emerald-500/20' : 'bg-amber-500/10 text-amber-500 border-amber-500/20';
            
            const card = document.createElement('div');
            card.className = "bg-white dark:bg-slate-900 rounded-none overflow-hidden group border-t border-b ltr:border-r rtl:border-l border-slate-200 dark:border-accent-dark hover:border-primary dark:hover:border-primary dark:hover:shadow-[0_0_30px_rgba(52,146,235,0.15)] shadow-none hover:shadow-2xl transition-all duration-300 mb-6";
            card.innerHTML = `
                <div class="flex flex-col md:flex-row">
                    <div class="w-full md:w-48 h-48 md:h-auto bg-cover bg-center transition-transform duration-500 group-hover:scale-110" style="background-image: url('${event.image || 'https://images.unsplash.com/photo-1511795409834-ef04bbd61622?q=80&w=2069&auto=format&fit=crop?q=80&w=2069&auto=format&fit=crop?q=80&w=800&auto=format&fit=crop'}')"></div>
                    <div class="flex-1 p-6 flex flex-col justify-between">
                        <div class="flex justify-between items-start">
                            <div>
                                <h4 class="text-lg font-bold text-slate-900 dark:text-white">${event.title}</h4>
                                <p class="text-primary font-bold text-xs mt-1">${event.title2}</p>
                            </div>
                            <span class="${statusClass} text-[10px] uppercase font-black px-2 py-1 rounded-full border tracking-widest">${event.status}</span>
                        </div>
                        <div class="grid grid-cols-2 gap-4 mt-6">
                            <div class="flex items-center gap-3">
                                <div class="size-9 bg-slate-100 dark:bg-slate-800 rounded-lg flex items-center justify-center text-slate-500">
                                    <span class="material-symbols-outlined text-[20px]">calendar_month</span>
                                </div>
                                <div>
                                    <p class="text-[10px] text-slate-500 uppercase font-black tracking-tighter">Date</p>
                                    <p class="text-xs font-bold">${dateStr}</p>
                                </div>
                            </div>
                            <div class="flex items-center gap-3">
                                <div class="size-9 bg-slate-100 dark:bg-slate-800 rounded-lg flex items-center justify-center text-slate-500">
                                    <span class="material-symbols-outlined text-[20px]">schedule</span>
                                </div>
                                <div>
                                    <p class="text-[10px] text-slate-500 uppercase font-black tracking-tighter">Time Slot</p>
                                    <p class="text-xs font-bold">${event.time}</p>
                                </div>
                            </div>
                        </div>
                        <div class="flex items-center justify-between mt-6 pt-4 border-t border-slate-100 dark:border-accent-dark">
                            <div class="flex items-center gap-2">
                                <div class="size-7 rounded-full border-2 border-primary overflow-hidden bg-slate-200">
                                    <img class="w-full h-full object-cover" src="${event.detailerImg || '../assets/images/user-placeholder.png'}" alt="Photographer"/>
                                </div>
                                <span class="text-[11px] text-slate-500 italic">Lead Photographer: ${event.photographer}</span>
                            </div>
                            <button class="text-slate-400 hover:text-primary transition-colors">
                                <span class="material-symbols-outlined">more_horiz</span>
                            </button>
                        </div>
                    </div>
                </div>
            `;
            container.appendChild(card);
        });
    };

    function createDayCell(day, isCurrentMonth, isToday = false, events = []) {
        const cell = document.createElement("div");
        cell.className = `bg-white dark:bg-slate-900 p-2 min-h-[90px] transition-all border-r border-b border-slate-100 dark:border-accent-dark/30 ${isCurrentMonth ? 'text-slate-900 dark:text-white' : 'text-slate-300 dark:text-slate-700'}`;
        
        let html = `
            <div class="flex justify-between items-start mb-1">
                <span class="text-[11px] font-bold ${isToday ? 'size-6 bg-primary text-white rounded-full flex items-center justify-center shadow-lg shadow-primary/20' : ''}">${day}</span>
            </div>
        `;

        if (events.length > 0) {
            events.forEach(event => {
                const colorClass = event.type === 'premium' ? 'bg-primary/10 border-primary/20 text-primary' : 
                                 event.type === 'maintenance' ? 'bg-amber-500/10 border-amber-500/20 text-amber-600' :
                                 'bg-emerald-500/10 border-emerald-500/20 text-emerald-600';
                
                html += `
                    <div class="p-1 px-1.5 ${colorClass} border rounded-md cursor-pointer hover:scale-[1.02] transition-transform mb-1 shadow-sm overflow-hidden">
                        <p class="text-[10px] font-bold truncate leading-tight">${event.title}</p>
                        ${event.title2 ? `<p class="text-[8px] opacity-70 truncate font-medium">${event.title2}</p>` : `<p class="text-[8px] opacity-70 truncate font-medium">${event.time}</p>`}
                    </div>
                `;
            });
        }

        cell.innerHTML = html;
        return cell;
    }

    window.renderCalendar = function(date) {
        const calendarGrid = document.getElementById("calendar-days");
        if (!calendarGrid) return;

        const month = date.getMonth();
        const year = date.getFullYear();

        // Update Title
        const monthYearString = date.toLocaleString("default", { month: "long", year: "numeric" });
        const titleEl = document.getElementById("calendar-title");
        if (titleEl) titleEl.innerText = monthYearString;

        // Clear Grid
        calendarGrid.innerHTML = "";

        // Get First Day of Month & Total Days
        const firstDayOfMonth = new Date(year, month, 1).getDay();
        const daysInMonth = new Date(year, month + 1, 0).getDate();
        
        // Prev Month Days
        const prevMonthLastDay = new Date(year, month, 0).getDate();
        
        // Total cells to fill (6 weeks = 42 cells)
        const totalCells = 42;

        // Today for highlighting
        const today = new Date();
        const isCurrentMonthToday = today.getMonth() === month && today.getFullYear() === year;

        // 1. Fill Leading Days (Prev Month)
        for (let i = firstDayOfMonth - 1; i >= 0; i--) {
            const day = prevMonthLastDay - i;
            calendarGrid.appendChild(createDayCell(day, false));
        }

        // 2. Fill Current Month Days
        for (let i = 1; i <= daysInMonth; i++) {
            const isToday = isCurrentMonthToday && today.getDate() === i;
            const events = calendarEvents.filter(e => 
                e.date.getDate() === i && 
                e.date.getMonth() === month && 
                e.date.getFullYear() === year
            );
            calendarGrid.appendChild(createDayCell(i, true, isToday, events));
        }

        // 3. Fill Trailing Days (Next Month)
        const currentCount = calendarGrid.children.length;
        for (let i = 1; i <= (totalCells - currentCount); i++) {
            calendarGrid.appendChild(createDayCell(i, false));
        }
    };

    window.nextMonth = function() {
        window.currentDate.setMonth(window.currentDate.getMonth() + 1);
        renderCalendar(window.currentDate);
    };

    window.prevMonth = function() {
        window.currentDate.setMonth(window.currentDate.getMonth() - 1);
        renderCalendar(window.currentDate);
    };

    // Form Submission Integration
    // Wait for some time to ensure modal and form are in the DOM if needed, 
    // though here they are static in the dashboard.html body
    setTimeout(() => {
        const appointmentForm = document.getElementById('appointment-form');
        if (appointmentForm) {
            appointmentForm.addEventListener('submit', function(e) {
                e.preventDefault();
                const formData = new FormData(this);
                
                // Get captured image DataURL (first one if multiple)
                const firstPreviewImg = document.querySelector('#image-preview-grid img');
                const capturedImageUrl = firstPreviewImg ? firstPreviewImg.src : null;

                // Create new event object
                const dateStr = formData.get('date');
                if (!dateStr) return;
                const [year, month, day] = dateStr.split('-').map(Number);
                
                const newEvent = {
                    date: new Date(year, month - 1, day),
                    title: `${formData.get('make')} ${formData.get('model')}`,
                    title2: formData.get('type') === 'premium' ? 'Editorial Portrait' : 
                            formData.get('type') === 'maintenance' ? 'Commercial Shoot' : 
                            formData.get('type') === 'interior' ? 'Product Photography' :
                            formData.get('type') === 'ppf' ? 'Event Coverage' :
                            formData.get('type') === 'recon' ? 'Headshot Session' :
                            formData.get('type') === 'tint' ? 'Photo Editing' : 'Digital Delivery',
                    type: formData.get('type'),
                    time: "10:00 AM - 04:00 PM",
                    photographer: "Alex Lumini", // Default photographer
                    detailerImg: "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?q=80&w=1974&auto=format&fit=crop",
                    status: "Pending",
                    image: capturedImageUrl
                };

                // Push to events list
                calendarEvents.push(newEvent);

                // Sync Views: Re-render calendar AND Upcoming cards
                renderCalendar(window.currentDate);
                renderUpcomingAppointments();

                // Visual Feedback
                const btn = this.querySelector('button[type="submit"]');
                const originalText = btn.innerHTML;
                btn.innerHTML = '<span class="material-symbols-outlined animate-spin text-[18px]">sync</span> Scheduling...';
                btn.disabled = true;

                setTimeout(() => {
                    btn.innerHTML = '<span class="material-symbols-outlined">check_circle</span> Scheduled!';
                    btn.classList.add('bg-emerald-500', 'shadow-emerald-500/20');
                    btn.classList.remove('bg-primary');

                    setTimeout(() => {
                        if (window.closeAppointmentModal) window.closeAppointmentModal();
                        
                        // Reset button for next time
                        setTimeout(() => {
                            btn.innerHTML = originalText;
                            btn.disabled = false;
                            btn.classList.remove('bg-emerald-500', 'shadow-emerald-500/20');
                            btn.classList.add('bg-primary');
                        }, 500);
                    }, 1500);
                }, 1000);
            });
        }
    }, 500);

    // Initial Load
    setTimeout(() => {
        if (document.getElementById("calendar-days")) {
            renderCalendar(window.currentDate);
        }
        renderUpcomingAppointments();
    }, 200);
});

// Modal and Global Functions (Exposed to Global Scope)
window.openAppointmentModal = function() {
    const modal = document.getElementById('appointment-modal');
    const container = document.getElementById('modal-container');
    if (!modal || !container) return;
    
    modal.classList.remove('hidden');
    modal.classList.add('flex');
    
    // Slight delay to trigger CSS transition
    setTimeout(() => {
        modal.classList.remove('opacity-0');
        modal.classList.add('opacity-100');
        container.classList.remove('scale-95');
        container.classList.add('scale-100');
    }, 10);
};

window.closeAppointmentModal = function() {
    const modal = document.getElementById('appointment-modal');
    const container = document.getElementById('modal-container');
    if (!modal || !container) return;

    modal.classList.add('opacity-0');
    modal.classList.remove('opacity-100');
    container.classList.add('scale-95');
    container.classList.remove('scale-100');
    
    setTimeout(() => {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
        // Reset form
        document.getElementById('appointment-form')?.reset();
        const grid = document.getElementById('image-preview-grid');
        if (grid) grid.innerHTML = '';
    }, 300);
};

window.handleImageUpload = function(input) {
    const grid = document.getElementById('image-preview-grid');
    if (!grid || !input.files) return;

    Array.from(input.files).forEach(file => {
        const reader = new FileReader();
        reader.onload = (e) => {
            const div = document.createElement('div');
            div.className = 'relative aspect-square rounded-xl overflow-hidden border border-slate-200 dark:border-white/10 group animate-in zoom-in duration-300';
            div.innerHTML = `
                <img src="${e.target.result}" class="w-full h-full object-cover">
                <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                    <span class="material-symbols-outlined text-white text-sm cursor-pointer hover:text-primary transition-colors" onclick="this.parentElement.parentElement.remove()">delete</span>
                </div>
            `;
            grid.appendChild(div);
        };
        reader.readAsDataURL(file);
    });
};

/* ============================================
   Custom Dropdown Logic (Multi-Instance Support)
   ============================================ */
document.addEventListener('click', (e) => {
    // Toggle Menu
    const trigger = e.target.closest('.premium-select-trigger');
    if (trigger) {
        const dropdown = trigger.closest('.premium-select');
        const menu = dropdown.querySelector('.premium-select-menu');
        
        // Close other open dropdowns first
        document.querySelectorAll('.premium-select').forEach(other => {
            if (other !== dropdown) {
                other.classList.remove('active');
                other.querySelector('.premium-select-menu')?.classList.remove('active', 'opacity-100');
                other.querySelector('.premium-select-menu')?.classList.add('opacity-0', 'invisible');
            }
        });

        // Toggle current
        const isActive = dropdown.classList.toggle('active');
        menu.classList.toggle('active', isActive);
        menu.classList.toggle('opacity-0', !isActive);
        menu.classList.toggle('opacity-100', isActive);
        menu.classList.toggle('invisible', !isActive);
        return;
    }

    // Handle Item Selection
    const item = e.target.closest('.dropdown-item');
    if (item) {
        const dropdown = item.closest('.premium-select');
        const menu = dropdown.querySelector('.premium-select-menu');
        const input = dropdown.querySelector('.premium-select-input');
        const selectedText = dropdown.querySelector('.selected-value');

        const val = item.getAttribute('data-value');
        const text = item.querySelector('span:last-child').textContent;

        // Update UI
        if (selectedText) selectedText.textContent = text;
        if (input) {
            input.value = val;
            // Trigger change event if needed
            input.dispatchEvent(new Event('change', { bubbles: true }));
        }
        
        // Close menu
        dropdown.classList.remove('active');
        menu.classList.remove('active', 'opacity-100');
        menu.classList.add('opacity-0', 'invisible');
        return;
    }

    // Close on outside click
    if (!e.target.closest('.premium-select')) {
        document.querySelectorAll('.premium-select').forEach(dropdown => {
            dropdown.classList.remove('active');
            const menu = dropdown.querySelector('.premium-select-menu');
            if (menu) {
                menu.classList.remove('active', 'opacity-100');
                menu.classList.add('opacity-0', 'invisible');
            }
        });
    }
});

/* ============================================
   Dashboard Navigation & Section Switching
   ============================================ */
window.switchSection = function(sectionId) {
    const contentArea = document.getElementById('dashboard-content');
    const template = document.getElementById('tmpl-' + sectionId);
    
    if (contentArea && template) {
        // Reset all regular nav links
        document.querySelectorAll('#sidebar-nav a').forEach(link => {
            link.classList.remove('bg-primary', 'text-white', 'font-bold', 'shadow-md', 'shadow-primary/20');
            link.classList.add('text-slate-500', 'dark:text-slate-400', 'hover:bg-slate-100', 'dark:hover:bg-accent-dark', 'font-medium');
        });

        // Reset bottom profile section
        const profileBottom = document.getElementById('nav-profile-bottom');
        if (profileBottom) {
            profileBottom.classList.remove('bg-primary/10', 'border', 'border-primary/20');
            profileBottom.classList.add('hover:bg-slate-100', 'dark:hover:bg-accent-dark');
        }

        // Reset mobile bottom nav links
        document.querySelectorAll('nav.md\\:hidden a.menu-item').forEach(link => {
            link.classList.remove('text-primary');
            link.classList.add('text-slate-500', 'dark:text-slate-400');
        });

        const activeLink = document.getElementById('nav-' + sectionId);
        const activeProfileBottom = (sectionId === 'profile') ? profileBottom : null;

        if (activeLink) {
            activeLink.classList.remove('text-slate-500', 'dark:text-slate-400', 'hover:bg-slate-100', 'dark:hover:bg-accent-dark', 'font-medium');
            activeLink.classList.add('bg-primary', 'text-white', 'font-bold', 'shadow-md', 'shadow-primary/20');
        }

        if (activeProfileBottom) {
            activeProfileBottom.classList.remove('hover:bg-slate-100', 'dark:hover:bg-accent-dark');
            activeProfileBottom.classList.add('bg-primary/10', 'border', 'border-primary/20');
        }

        // Activate mobile bottom nav link
        const bottomNavLink = document.querySelector(`nav.md\\:hidden a[href="#${sectionId}"]`);
        if (bottomNavLink) {
            bottomNavLink.classList.remove('text-slate-500', 'dark:text-slate-400');
            bottomNavLink.classList.add('text-primary');
        }

        // Update Global Header Title/Subtitle (if they exist)
        const headerTitle = document.getElementById('section-title');
        const headerSubtitle = document.getElementById('section-subtitle');

        const titles = {
            'overview': 'Dashboard Overview',
            'orders': 'Booking History',
            'saved': 'Saved Services',
            'messages': 'Communications',
            'settings': 'Dashboard Settings',
            'profile': 'Profile Management',
            'projects': 'My Projects',
            'appointments': 'Studio Sessions',
            'history': 'Project History',
            'invoices': 'Financial Records'
        };

        const subtitles = {
            'overview': 'Welcome back! Your photography studio at a glance.',
            'orders': 'Review your previous and upcoming photography sessions.',
            'saved': "Keep track of photography packages you're interested in.",
            'messages': 'Stay connected with the studio and your clients.',
            'settings': 'Manage your account preferences and studio settings.',
            'profile': 'Manage your photography profile and preferences.',
            'projects': 'Manage and track your active photography projects.',
            'appointments': 'Manage your studio bookings and location shoot schedule.',
            'history': 'Detailed session logs and project history for your creative work.',
            'invoices': 'Manage and track your photography project billings.'
        };

        if (headerTitle && titles[sectionId]) headerTitle.textContent = titles[sectionId];
        if (headerSubtitle && subtitles[sectionId]) headerSubtitle.textContent = subtitles[sectionId];

        contentArea.innerHTML = template.innerHTML;
        window.location.hash = sectionId;
        window.scrollTo(0, 0);

        // Re-initialize dynamic components based on section
        if (sectionId === 'appointments') {
            if (window.renderUpcomingAppointments) window.renderUpcomingAppointments();
            if (window.renderCalendar) window.renderCalendar(window.currentDate || new Date());
        }
    }
};

// Handle initial load and hash changes for dashboard
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('dashboard-content')) {
        const hash = window.location.hash.replace('#', '');
        window.switchSection(hash && document.getElementById('tmpl-' + hash) ? hash : 'overview');
    }
});

window.addEventListener('hashchange', () => {
    if (document.getElementById('dashboard-content')) {
        const hash = window.location.hash.replace('#', '');
        if (hash && document.getElementById('tmpl-' + hash)) window.switchSection(hash);
    }
});







document.addEventListener('DOMContentLoaded', function() {

    // ----------------------------------------------------
    // 1. Mobile Menu (Hamburger Menu) Code - كود قائمة الموبايل (الهامبرغر)
    // ----------------------------------------------------
    const menuToggle = document.getElementById('menuToggle');
    const mobileMenu = document.getElementById('mobileMenu');
    // تأكد من وجود عنصر HTML بـ id="overlay" في ملف HTML الخاص بك
    const overlay = document.getElementById('overlay');
    const closeMenu = document.getElementById('closeMenu');
    const hamburgerLines = document.querySelectorAll('.hamburger-line');
    const navItems = document.querySelectorAll('.mobile-nav-item');

    let isMenuOpen = false;

    // دالة لفتح قائمة الموبايل
    function openMenu() {
        mobileMenu.classList.add('open');
        if (overlay) overlay.classList.add('active'); // تفعيل التراكب إذا كان موجوداً
        menuToggle.classList.add('active'); // تغيير شكل أيقونة الهامبرغر
        menuToggle.setAttribute('aria-expanded', 'true');
        isMenuOpen = true;

        // تطبيق تأثيرات التحويل على خطوط الهامبرغر
        hamburgerLines.forEach((line, index) => {
            line.style.transition = 'all 0.4s ease';
            if (index === 0) {
                line.style.transform = 'translateY(8px) rotate(45deg)';
            } else if (index === 1) {
                line.style.opacity = '0'; // إخفاء الخط الأوسط
            } else {
                line.style.transform = 'translateY(-8px) rotate(-45deg)';
            }
        });
    }

    // دالة لإغلاق قائمة الموبايل
    function closeMenuHandler() {
        mobileMenu.classList.remove('open');
        if (overlay) overlay.classList.remove('active'); // إخفاء التراكب إذا كان موجوداً
        menuToggle.classList.remove('active'); // إعادة أيقونة الهامبرغر لوضعها الطبيعي
        menuToggle.setAttribute('aria-expanded', 'false');
        isMenuOpen = false;

        // إعادة خطوط الهامبرغر لوضعها الأصلي
        hamburgerLines.forEach(line => {
            line.style.transform = '';
            line.style.opacity = '';
        });
    }

    // إضافة مستمعي الأحداث لعناصر قائمة الموبايل
    if (menuToggle && mobileMenu && closeMenu) {
        menuToggle.addEventListener('click', function() {
            if (!isMenuOpen) {
                openMenu();
            } else {
                closeMenuHandler();
            }
        });

        closeMenu.addEventListener('click', closeMenuHandler);

        if (overlay) {
            overlay.addEventListener('click', closeMenuHandler); // إغلاق القائمة عند النقر على التراكب
        }

        // إغلاق قائمة الموبايل عند النقر على عنصر داخلها (ما لم يكن له قائمة فرعية)
        navItems.forEach(item => {
            item.addEventListener('click', function() {
                // إذا كان العنصر يحتوي على مؤشر قائمة فرعية (مثل ▼ أو +)، فلا تغلق القائمة الرئيسية
                if (this.textContent.includes('▼') || this.textContent.includes('+')) {
                    // يمكنك إضافة منطق لفتح القائمة الفرعية هنا إذا لم يكن موجودًا
                    return;
                }
                closeMenuHandler(); // إغلاق القائمة بعد النقر على عنصر عادي
            });
        });

        // إغلاق قائمة الموبايل إذا تم تغيير حجم الشاشة لتصبح أكبر من شاشة الموبايل
        window.addEventListener('resize', function() {
            if (window.innerWidth > 768 && isMenuOpen) {
                closeMenuHandler();
            }
        });

        // دعم التنقل بلوحة المفاتيح لأزرار قائمة الموبايل
        menuToggle.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.click();
            }
        });

        closeMenu.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.click();
            }
        });
    }


    // ----------------------------------------------------
    // 2. User Dropdown Menu Code - كود القائمة المنسدلة للمستخدم
    // ----------------------------------------------------
    const userMenuContainer = document.querySelector('.user-menu-container');
    const userIconTrigger = document.querySelector('.user-icon-trigger');
    const userDropdownMenu = document.querySelector('.user-dropdown-menu');

    // إضافة مستمعي الأحداث لقائمة المستخدم المنسدلة
    if (userIconTrigger && userDropdownMenu && userMenuContainer) {
        userIconTrigger.addEventListener('click', function(e) {
            e.preventDefault(); // منع سلوك الرابط الافتراضي
            e.stopPropagation(); // منع انتشار الحدث ليمنع إغلاق القائمة فورًا عند النقر عليها
            userDropdownMenu.classList.toggle('active'); // تبديل فئة 'active' لإظهار/إخفاء القائمة
        });

        // إخفاء القائمة عند النقر خارجها
        document.addEventListener('click', function(e) {
            // التحقق إذا كان النقر خارج حاوية القائمة المنسدلة بأكملها
            if (!userMenuContainer.contains(e.target) && userDropdownMenu.classList.contains('active')) {
                userDropdownMenu.classList.remove('active');
            }
        });
    }

    // ----------------------------------------------------
    // 3. General Dropdown Menus Code (if any) - كود القوائم المنسدلة العامة (إذا وجدت)
    // ----------------------------------------------------
    // ملاحظة: هذا الجزء من الكود يعالج أي قوائم منسدلة أخرى لها فئة 'dropdown' وتحتوي على '.dropdown-menu'.
    // إذا كنت تستخدم نفس الفئات (مثل .dropdown-menu) لقائمة المستخدم، قد تحتاج إلى توحيد طريقة التعامل
    // مع جميع القوائم المنسدلة لتجنب التعارض.
    const dropdowns = document.querySelectorAll('.dropdown');
    dropdowns.forEach(dropdown => {
        dropdown.addEventListener('click', function(e) {
            e.stopPropagation(); // منع انتشار الحدث
            const menu = this.querySelector('.dropdown-menu');
            if (menu) {
                if (menu.style.display === 'block') {
                    menu.style.display = 'none';
                } else {
                    // إغلاق جميع القوائم المنسدلة الأخرى قبل فتح هذه القائمة
                    document.querySelectorAll('.dropdown-menu').forEach(otherMenu => {
                        if (otherMenu !== menu) {
                            otherMenu.style.display = 'none';
                        }
                    });
                    menu.style.display = 'block';
                }
            }
        });
    });

    // إغلاق القوائم المنسدلة العامة عند النقر خارجها
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.dropdown')) { // إذا لم يكن النقر داخل أي عنصر ذي فئة 'dropdown'
            const allDropdownMenus = document.querySelectorAll('.dropdown-menu');
            allDropdownMenus.forEach(menu => {
                menu.style.display = 'none';
            });
        }
    });

    // ----------------------------------------------------
    // 4. Search Bar Toggle Logic - منطق تبديل شريط البحث
    // ----------------------------------------------------
    const searchIcon = document.getElementById('searchIcon');
    const searchBarContainer = document.getElementById('searchBarContainer');

    // إضافة مستمعي الأحداث لأيقونة البحث وشريط البحث
    if (searchIcon && searchBarContainer) {
        searchIcon.addEventListener('click', function(event) {
            event.stopPropagation(); // منع انتشار الحدث عند النقر على الأيقونة
            // التحقق مما إذا كان شريط البحث نشطًا حاليًا
            const isActive = searchBarContainer.classList.contains('active');

            if (isActive) {
                // إذا كان نشطًا، قم بإخفائه وأظهر الأيقونة
                searchBarContainer.classList.remove('active');
                searchIcon.classList.remove('hidden');
            } else {
                // إذا كان مخفيًا، قم بإخفاء الأيقونة وإظهار شريط البحث
                searchIcon.classList.add('hidden');
                searchBarContainer.classList.add('active');
            }
        });

        // إغلاق شريط البحث عند النقر خارج (اختياري، لكن يوفر تجربة مستخدم جيدة)
        document.addEventListener('click', function(event) {
            // التحقق مما إذا كان النقر خارج أيقونة البحث وحاوية شريط البحث
            if (!searchIcon.contains(event.target) && !searchBarContainer.contains(event.target)) {
                if (searchBarContainer.classList.contains('active')) {
                    searchBarContainer.classList.remove('active');
                    searchIcon.classList.remove('hidden'); // إعادة إظهار أيقونة البحث
                }
            }
        });
    }
});
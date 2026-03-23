/**
 * Motion System
 * Purposeful animations with spring physics
 */

const MotionSystem = {
  // Configuration
  config: {
    spring: { tension: 300, friction: 30 },
    easeOutExpo: 'cubic-bezier(0.16, 1, 0.3, 1)',
    easeOutQuart: 'cubic-bezier(0.25, 1, 0.5, 1)',
    duration: {
      fast: 150,
      base: 250,
      slow: 400,
      slower: 600
    }
  },
  
  // Initialize motion system
  init() {
    this.observeElements();
    this.bindInteractions();
  },
  
  // Intersection Observer for entrance animations
  observeElements() {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          this.animateEntrance(entry.target);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });
    
    document.querySelectorAll('.motion-entrance').forEach(el => {
      el.style.opacity = '0';
      el.style.transform = 'translateY(20px)';
      observer.observe(el);
    });
  },
  
  // Entrance animation
  animateEntrance(element) {
    const delay = element.dataset.delay || 0;
    
    element.style.transition = `opacity ${this.config.duration.slow}ms ${this.config.easeOutExpo}, 
                                transform ${this.config.duration.slow}ms ${this.config.easeOutExpo}`;
    element.style.transitionDelay = `${delay}ms`;
    
    requestAnimationFrame(() => {
      element.style.opacity = '1';
      element.style.transform = 'translateY(0)';
    });
  },
  
  // Staggered reveal for containers
  staggerReveal(container, selector = '.stagger-item') {
    const items = container.querySelectorAll(selector);
    items.forEach((item, i) => {
      item.style.opacity = '0';
      item.style.transform = 'translateY(20px)';
      
      setTimeout(() => {
        item.style.transition = `opacity ${this.config.duration.slow}ms ${this.config.easeOutExpo},
                                transform ${this.config.duration.slow}ms ${this.config.easeOutExpo}`;
        item.style.opacity = '1';
        item.style.transform = 'translateY(0)';
      }, i * 50);
    });
  },
  
  // Number count-up animation
  countUp(element, target, duration = 1000, suffix = '') {
    const start = 0;
    const startTime = performance.now();
    
    const animate = (currentTime) => {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      
      // Ease out expo
      const easeProgress = 1 - Math.pow(1 - progress, 4);
      const current = Math.round(start + (target - start) * easeProgress);
      
      element.textContent = current + suffix;
      
      if (progress < 1) {
        requestAnimationFrame(animate);
      }
    };
    
    requestAnimationFrame(animate);
  },
  
  // Gauge/progress animation
  animateGauge(element, targetPercent, duration = 800) {
    const circumference = 2 * Math.PI * element.r.baseVal.value;
    const targetOffset = circumference - (targetPercent / 100) * circumference;
    
    element.style.transition = `stroke-dashoffset ${duration}ms ${this.config.easeOutExpo}`;
    element.style.strokeDasharray = circumference;
    element.style.strokeDashoffset = circumference;
    
    requestAnimationFrame(() => {
      element.style.strokeDashoffset = targetOffset;
    });
  },
  
  // Progress bar animation
  animateProgress(element, targetPercent, duration = 600) {
    element.style.transition = `width ${duration}ms ${this.config.easeOutExpo}`;
    element.style.width = '0%';
    
    requestAnimationFrame(() => {
      element.style.width = `${targetPercent}%`;
    });
  },
  
  // Magnetic button effect
  bindMagneticButtons() {
    document.querySelectorAll('.btn-magnetic').forEach(btn => {
      btn.addEventListener('mousemove', (e) => {
        const rect = btn.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;
        
        btn.style.transform = `translate(${x * 0.2}px, ${y * 0.2}px)`;
      });
      
      btn.addEventListener('mouseleave', () => {
        btn.style.transition = `transform ${this.config.duration.base}ms ${this.config.easeOutExpo}`;
        btn.style.transform = 'translate(0, 0)';
        
        setTimeout(() => {
          btn.style.transition = '';
        }, this.config.duration.base);
      });
    });
  },
  
  // Ripple effect on click
  createRipple(e, element) {
    const ripple = document.createElement('span');
    const rect = element.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    
    ripple.style.cssText = `
      position: absolute;
      border-radius: 50%;
      background: currentColor;
      opacity: 0.3;
      width: ${size}px;
      height: ${size}px;
      left: ${e.clientX - rect.left - size / 2}px;
      top: ${e.clientY - rect.top - size / 2}px;
      pointer-events: none;
      transform: scale(0);
      transition: transform 600ms ${this.config.easeOutExpo}, opacity 600ms ease;
    `;
    
    element.style.position = 'relative';
    element.style.overflow = 'hidden';
    element.appendChild(ripple);
    
    requestAnimationFrame(() => {
      ripple.style.transform = 'scale(2)';
      ripple.style.opacity = '0';
    });
    
    setTimeout(() => ripple.remove(), 600);
  },
  
  // Bind all interactions
  bindInteractions() {
    this.bindMagneticButtons();
    
    // Ripple on buttons
    document.querySelectorAll('.btn').forEach(btn => {
      btn.addEventListener('click', (e) => this.createRipple(e, btn));
    });
    
    // Card hover lift
    document.querySelectorAll('.card-hover-lift').forEach(card => {
      card.addEventListener('mouseenter', () => {
        card.style.transition = `transform ${this.config.duration.base}ms ${this.config.easeOutExpo},
                                box-shadow ${this.config.duration.base}ms ${this.config.easeOutExpo}`;
        card.style.transform = 'translateY(-4px)';
      });
      
      card.addEventListener('mouseleave', () => {
        card.style.transform = 'translateY(0)';
      });
    });
    
    // Tab switching animation
    document.querySelectorAll('.tab-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const tabId = btn.dataset.tab;
        this.switchTab(tabId);
      });
    });
  },
  
  // Tab switch with animation
  switchTab(tabId) {
    const currentTab = document.querySelector('.tab-content.active');
    const newTab = document.getElementById(tabId);
    
    if (currentTab === newTab) return;
    
    // Fade out current
    if (currentTab) {
      currentTab.style.transition = `opacity ${this.config.duration.fast}ms ease`;
      currentTab.style.opacity = '0';
      
      setTimeout(() => {
        currentTab.classList.remove('active');
        
        // Fade in new
        newTab.classList.add('active');
        newTab.style.opacity = '0';
        
        requestAnimationFrame(() => {
          newTab.style.transition = `opacity ${this.config.duration.slow}ms ${this.config.easeOutExpo}`;
          newTab.style.opacity = '1';
          
          // Stagger reveal children
          this.staggerReveal(newTab);
        });
      }, this.config.duration.fast);
    } else {
      newTab.classList.add('active');
      newTab.style.opacity = '1';
    }
  },
  
  // Scroll-triggered parallax
  bindParallax() {
    const parallaxElements = document.querySelectorAll('.parallax');
    
    const handleScroll = () => {
      const scrollY = window.scrollY;
      
      parallaxElements.forEach(el => {
        const speed = parseFloat(el.dataset.speed) || 0.5;
        el.style.transform = `translateY(${scrollY * speed}px)`;
      });
    };
    
    window.addEventListener('scroll', handleScroll, { passive: true });
  },
  
  // Pulse animation for live indicators
  pulse(element) {
    element.style.animation = 'pulse 2s ease-in-out infinite';
  }
};

// CSS keyframes injection
const style = document.createElement('style');
style.textContent = `
  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
  }
  
  @keyframes shimmer {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
  }
  
  @keyframes slideUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
  }
  
  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }
  
  .motion-entrance {
    will-change: opacity, transform;
  }
  
  .stagger-item {
    will-change: opacity, transform;
  }
`;
document.head.appendChild(style);

// Export
if (typeof module !== 'undefined') module.exports = MotionSystem;

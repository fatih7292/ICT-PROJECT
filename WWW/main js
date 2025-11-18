// Feedback System - Main JavaScript File

// Mock Data
const professorsData = [
    {
        id: 1,
        name: "Dr. Sarah Johnson",
        subject: "Computer Science",
        university: "Stanford University",
        image: "resources/professor-1.jpg",
        rating: 4.9,
        reviewCount: 127,
        specialties: ["Artificial Intelligence", "Machine Learning"],
        bio: "Leading researcher in AI with 15 years of teaching experience.",
        reviews: [
            {
                id: 1,
                author: "Student123",
                rating: 5,
                date: "2024-01-15",
                course: "CS101",
                text: "Excellent professor with clear explanations and engaging lectures. Highly recommended!",
                helpful: 23,
                anonymous: true
            },
            {
                id: 2,
                author: "CS_Major",
                rating: 5,
                date: "2024-01-10",
                course: "CS201",
                text: "Dr. Johnson makes complex topics easy to understand. Her passion for AI is infectious.",
                helpful: 18,
                anonymous: false
            }
        ]
    },
    {
        id: 2,
        name: "Prof. Michael Chen",
        subject: "Mathematics",
        university: "MIT",
        image: "resources/professor-2.jpg",
        rating: 4.7,
        reviewCount: 89,
        specialties: ["Calculus", "Linear Algebra"],
        bio: "Award-winning mathematician with a gift for making math accessible.",
        reviews: [
            {
                id: 3,
                author: "Math_Lover",
                rating: 4,
                date: "2024-01-12",
                course: "MATH201",
                text: "Great professor but moves through material quickly. Be prepared to study!",
                helpful: 15,
                anonymous: true
            }
        ]
    },
    {
        id: 3,
        name: "Dr. Emily Rodriguez",
        subject: "Physics",
        university: "Caltech",
        image: "resources/professor-3.jpg",
        rating: 4.8,
        reviewCount: 156,
        specialties: ["Quantum Mechanics", "Particle Physics"],
        bio: "Brilliant physicist who brings energy and excitement to every lecture.",
        reviews: [
            {
                id: 4,
                author: "Physics_Student",
                rating: 5,
                date: "2024-01-08",
                course: "PHYS301",
                text: "Dr. Rodriguez is amazing! Her demonstrations make physics come alive.",
                helpful: 31,
                anonymous: false
            }
        ]
    },
    {
        id: 4,
        name: "Prof. David Kim",
        subject: "Chemistry",
        university: "Harvard University",
        image: "resources/professor-4.jpg",
        rating: 4.6,
        reviewCount: 98,
        specialties: ["Organic Chemistry", "Biochemistry"],
        bio: "Dedicated teacher with innovative lab techniques and real-world applications.",
        reviews: []
    },
    {
        id: 5,
        name: "Dr. Lisa Thompson",
        subject: "Biology",
        university: "Yale University",
        image: "resources/professor-5.jpg",
        rating: 4.9,
        reviewCount: 203,
        specialties: ["Genetics", "Molecular Biology"],
        bio: "Passionate biologist who inspires students to explore the natural world.",
        reviews: []
    },
    {
        id: 6,
        name: "Prof. James Wilson",
        subject: "English Literature",
        university: "Oxford University",
        image: "resources/professor-6.jpg",
        rating: 4.5,
        reviewCount: 74,
        specialties: ["Shakespeare", "Modern Literature"],
        bio: "Literary scholar with a talent for making classic literature relevant today.",
        reviews: []
    }
];

const studentAvatars = [
    "resources/student-avatars/avatar-1.jpg",
    "resources/student-avatars/avatar-2.jpg",
    "resources/student-avatars/avatar-3.jpg",
    "resources/student-avatars/avatar-4.jpg",
    "resources/student-avatars/avatar-5.jpg",
    "resources/student-avatars/avatar-6.jpg"
];

// Global Variables
let currentRating = 0;
let searchResults = [];
let filteredProfessors = [...professorsData];

// Initialize Application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Initialize typewriter effect
    initializeTypewriter();
    
    // Initialize particle background
    initializeParticles();
    
    // Initialize carousel
    initializeCarousel();
    
    // Populate featured professors
    populateFeaturedProfessors();
    
    // Populate top professors
    populateTopProfessors();
    
    // Initialize search functionality
    initializeSearch();
    
    // Initialize review form
    initializeReviewForm();
    
    // Initialize scroll animations
    initializeScrollAnimations();
    
    // Animate counters
    animateCounters();
}

function initializeTypewriter() {
    const typed = new Typed('#typed-text', {
        strings: [
            'Rate Your Professors',
            'Share Your Experience',
            'Help Other Students',
            'Make Better Choices'
        ],
        typeSpeed: 80,
        backSpeed: 50,
        backDelay: 2000,
        loop: true,
        showCursor: true,
        cursorChar: '|'
    });
}

function initializeParticles() {
    const canvas = document.getElementById('particleCanvas');
    if (!canvas) return;
    
    // p5.js sketch for particle background
    new p5(function(p) {
        let particles = [];
        let connections = [];
        
        p.setup = function() {
            p.createCanvas(p.windowWidth, p.windowHeight);
            
            // Create particles
            for (let i = 0; i < 50; i++) {
                particles.push({
                    x: p.random(p.width),
                    y: p.random(p.height),
                    vx: p.random(-0.5, 0.5),
                    vy: p.random(-0.5, 0.5),
                    size: p.random(2, 4)
                });
            }
        };
        
        p.draw = function() {
            p.clear();
            
            // Update and draw particles
            for (let particle of particles) {
                particle.x += particle.vx;
                particle.y += particle.vy;
                
                // Wrap around edges
                if (particle.x < 0) particle.x = p.width;
                if (particle.x > p.width) particle.x = 0;
                if (particle.y < 0) particle.y = p.height;
                if (particle.y > p.height) particle.y = 0;
                
                // Draw particle
                p.fill(255, 255, 255, 100);
                p.noStroke();
                p.ellipse(particle.x, particle.y, particle.size);
            }
            
            // Draw connections
            p.stroke(255, 255, 255, 50);
            p.strokeWeight(1);
            
            for (let i = 0; i < particles.length; i++) {
                for (let j = i + 1; j < particles.length; j++) {
                    let dist = p.dist(particles[i].x, particles[i].y, particles[j].x, particles[j].y);
                    if (dist < 100) {
                        p.line(particles[i].x, particles[i].y, particles[j].x, particles[j].y);
                    }
                }
            }
        };
        
        p.windowResized = function() {
            p.resizeCanvas(p.windowWidth, p.windowHeight);
        };
    }, canvas);
}

function initializeCarousel() {
    const splide = new Splide('#featuredCarousel', {
        type: 'loop',
        perPage: 3,
        perMove: 1,
        gap: '2rem',
        autoplay: true,
        interval: 4000,
        pauseOnHover: true,
        breakpoints: {
            768: {
                perPage: 1,
            },
            1024: {
                perPage: 2,
            }
        }
    });
    
    splide.mount();
}

function populateFeaturedProfessors() {
    const container = document.getElementById('featuredProfessors');
    if (!container) return;
    
    const featuredProfessors = professorsData.slice(0, 4);
    
    container.innerHTML = featuredProfessors.map(prof => `
        <li class="splide__slide">
            <div class="professor-card bg-white rounded-2xl p-6 shadow-lg h-full">
                <div class="flex items-center mb-4">
                    <img src="${prof.image}" alt="${prof.name}" class="w-16 h-16 rounded-full object-cover mr-4">
                    <div>
                        <h3 class="text-xl font-semibold text-gray-900">${prof.name}</h3>
                        <p class="text-gray-600">${prof.subject}</p>
                        <p class="text-sm text-gray-500">${prof.university}</p>
                    </div>
                </div>
                <div class="flex items-center mb-3">
                    <div class="rating-stars text-lg mr-2">
                        ${generateStars(prof.rating)}
                    </div>
                    <span class="text-gray-700 font-semibold">${prof.rating}</span>
                    <span class="text-gray-500 text-sm ml-2">(${prof.reviewCount} reviews)</span>
                </div>
                <p class="text-gray-600 text-sm mb-4">${prof.bio}</p>
                <div class="flex flex-wrap gap-2 mb-4">
                    ${prof.specialties.map(spec => `
                        <span class="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full">${spec}</span>
                    `).join('')}
                </div>
                <button onclick="viewProfessor(${prof.id})" class="w-full bg-navy text-white py-2 rounded-lg hover:bg-blue-800 transition-colors">
                    View Profile
                </button>
            </div>
        </li>
    `).join('');
}

function populateTopProfessors() {
    const container = document.getElementById('topProfessors');
    if (!container) return;
    
    const topProfessors = [...professorsData]
        .sort((a, b) => b.rating - a.rating)
        .slice(0, 6);
    
    container.innerHTML = topProfessors.map(prof => `
        <div class="professor-card bg-white rounded-2xl p-6 shadow-lg fade-in">
            <div class="flex items-center mb-4">
                <img src="${prof.image}" alt="${prof.name}" class="w-16 h-16 rounded-full object-cover mr-4">
                <div class="flex-1">
                    <h3 class="text-xl font-semibold text-gray-900">${prof.name}</h3>
                    <p class="text-gray-600">${prof.subject}</p>
                    <p class="text-sm text-gray-500">${prof.university}</p>
                </div>
            </div>
            <div class="flex items-center mb-3">
                <div class="rating-stars text-lg mr-2">
                    ${generateStars(prof.rating)}
                </div>
                <span class="text-gray-700 font-semibold">${prof.rating}</span>
                <span class="text-gray-500 text-sm ml-2">(${prof.reviewCount} reviews)</span>
            </div>
            <p class="text-gray-600 text-sm mb-4">${prof.bio}</p>
            <button onclick="viewProfessor(${prof.id})" class="w-full bg-navy text-white py-2 rounded-lg hover:bg-blue-800 transition-colors">
                View Profile
            </button>
        </div>
    `).join('');
}

function initializeSearch() {
    const searchInput = document.getElementById('searchInput');
    const subjectFilter = document.getElementById('subjectFilter');
    const sortBy = document.getElementById('sortBy');
    
    if (searchInput) {
        searchInput.addEventListener('input', debounce(handleSearch, 300));
    }
    
    if (subjectFilter) {
        subjectFilter.addEventListener('change', handleFilter);
    }
    
    if (sortBy) {
        sortBy.addEventListener('change', handleSort);
    }
}

function handleSearch(query) {
    if (!query.trim()) {
        hideSearchResults();
        return;
    }
    
    const filtered = professorsData.filter(prof => 
        prof.name.toLowerCase().includes(query.toLowerCase()) ||
        prof.subject.toLowerCase().includes(query.toLowerCase()) ||
        prof.university.toLowerCase().includes(query.toLowerCase())
    );
    
    filteredProfessors = filtered;
    displaySearchResults(filtered);
}

function handleFilter() {
    const subject = document.getElementById('subjectFilter').value;
    const searchQuery = document.getElementById('searchInput').value;
    
    let filtered = [...professorsData];
    
    if (searchQuery.trim()) {
        filtered = filtered.filter(prof => 
            prof.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
            prof.subject.toLowerCase().includes(searchQuery.toLowerCase()) ||
            prof.university.toLowerCase().includes(searchQuery.toLowerCase())
        );
    }
    
    if (subject) {
        filtered = filtered.filter(prof => prof.subject === subject);
    }
    
    filteredProfessors = filtered;
    displaySearchResults(filtered);
}

function handleSort() {
    const sortBy = document.getElementById('sortBy').value;
    
    let sorted = [...filteredProfessors];
    
    switch (sortBy) {
        case 'rating':
            sorted.sort((a, b) => b.rating - a.rating);
            break;
        case 'name':
            sorted.sort((a, b) => a.name.localeCompare(b.name));
            break;
        case 'reviews':
            sorted.sort((a, b) => b.reviewCount - a.reviewCount);
            break;
    }
    
    displaySearchResults(sorted);
}

function displaySearchResults(professors) {
    const searchResultsSection = document.getElementById('searchResults');
    const resultsGrid = document.getElementById('searchResultsGrid');
    
    if (!searchResultsSection || !resultsGrid) return;
    
    if (professors.length === 0) {
        resultsGrid.innerHTML = `
            <div class="col-span-full text-center py-12">
                <div class="text-gray-400 text-6xl mb-4">🔍</div>
                <h3 class="text-xl font-semibold text-gray-900 mb-2">No professors found</h3>
                <p class="text-gray-600">Try adjusting your search criteria</p>
            </div>
        `;
    } else {
        resultsGrid.innerHTML = professors.map(prof => `
            <div class="professor-card bg-white rounded-2xl p-6 shadow-lg">
                <div class="flex items-center mb-4">
                    <img src="${prof.image}" alt="${prof.name}" class="w-16 h-16 rounded-full object-cover mr-4">
                    <div class="flex-1">
                        <h3 class="text-xl font-semibold text-gray-900">${prof.name}</h3>
                        <p class="text-gray-600">${prof.subject}</p>
                        <p class="text-sm text-gray-500">${prof.university}</p>
                    </div>
                </div>
                <div class="flex items-center mb-3">
                    <div class="rating-stars text-lg mr-2">
                        ${generateStars(prof.rating)}
                    </div>
                    <span class="text-gray-700 font-semibold">${prof.rating}</span>
                    <span class="text-gray-500 text-sm ml-2">(${prof.reviewCount} reviews)</span>
                </div>
                <p class="text-gray-600 text-sm mb-4">${prof.bio}</p>
                <div class="flex flex-wrap gap-2 mb-4">
                    ${prof.specialties.map(spec => `
                        <span class="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full">${spec}</span>
                    `).join('')}
                </div>
                <button onclick="viewProfessor(${prof.id})" class="w-full bg-navy text-white py-2 rounded-lg hover:bg-blue-800 transition-colors">
                    View Profile
                </button>
            </div>
        `).join('');
    }
    
    searchResultsSection.classList.remove('hidden');
    searchResultsSection.scrollIntoView({ behavior: 'smooth' });
}

function hideSearchResults() {
    const searchResultsSection = document.getElementById('searchResults');
    if (searchResultsSection) {
        searchResultsSection.classList.add('hidden');
    }
}

function performSearch() {
    const searchQuery = document.getElementById('searchInput').value;
    handleSearch(searchQuery);
}

function initializeReviewForm() {
    const ratingStars = document.querySelectorAll('.star');
    const reviewText = document.getElementById('reviewText');
    
    // Initialize rating stars
    ratingStars.forEach(star => {
        star.addEventListener('click', function() {
            const rating = parseInt(this.dataset.rating);
            setRating(rating);
        });
        
        star.addEventListener('mouseover', function() {
            const rating = parseInt(this.dataset.rating);
            highlightStars(rating);
        });
    });
    
    document.querySelector('.rating-input').addEventListener('mouseleave', function() {
        highlightStars(currentRating);
    });
    
    // Character counter for review text
    if (reviewText) {
        reviewText.addEventListener('input', function() {
            const count = this.value.length;
            document.getElementById('charCount').textContent = count;
            
            if (count > 500) {
                this.value = this.value.substring(0, 500);
                document.getElementById('charCount').textContent = 500;
            }
        });
    }
}

function setRating(rating) {
    currentRating = rating;
    highlightStars(rating);
    updateRatingText(rating);
}

function highlightStars(rating) {
    const stars = document.querySelectorAll('.star');
    stars.forEach((star, index) => {
        if (index < rating) {
            star.classList.remove('text-gray-300');
            star.classList.add('text-gold');
        } else {
            star.classList.remove('text-gold');
            star.classList.add('text-gray-300');
        }
    });
}

function updateRatingText(rating) {
    const ratingText = document.getElementById('ratingText');
    const ratingTexts = ['', 'Poor', 'Fair', 'Good', 'Very Good', 'Excellent'];
    ratingText.textContent = ratingTexts[rating] || 'Click to rate';
}

function initializeScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);
    
    document.querySelectorAll('.fade-in').forEach(el => {
        observer.observe(el);
    });
}

function animateCounters() {
    const counters = [
        { id: 'professorCount', target: 2847 },
        { id: 'reviewCount', target: 15234 },
        { id: 'universityCount', target: 156 }
    ];
    
    counters.forEach(counter => {
        const element = document.getElementById(counter.id);
        if (!element) return;
        
        anime({
            targets: { count: 0 },
            count: counter.target,
            duration: 2000,
            delay: 500,
            easing: 'easeOutQuart',
            update: function(anim) {
                element.textContent = Math.floor(anim.animatables[0].target.count).toLocaleString();
            }
        });
    });
}

function generateStars(rating) {
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 >= 0.5;
    const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);
    
    let stars = '';
    
    // Full stars
    for (let i = 0; i < fullStars; i++) {
        stars += '<span class="text-gold">★</span>';
    }
    
    // Half star
    if (hasHalfStar) {
        stars += '<span class="text-gold">☆</span>';
    }
    
    // Empty stars
    for (let i = 0; i < emptyStars; i++) {
        stars += '<span class="text-gray-300">★</span>';
    }
    
    return stars;
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Modal Functions
function showAddReview() {
    const modal = document.getElementById('addReviewModal');
    if (modal) {
        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    }
}

function closeAddReview() {
    const modal = document.getElementById('addReviewModal');
    if (modal) {
        modal.classList.add('hidden');
        document.body.style.overflow = 'auto';
        resetReviewForm();
    }
}

function resetReviewForm() {
    document.getElementById('reviewForm').reset();
    currentRating = 0;
    highlightStars(0);
    updateRatingText(0);
    document.getElementById('charCount').textContent = '0';
}

function submitReview(event) {
    event.preventDefault();
    
    if (currentRating === 0) {
        alert('Please select a rating before submitting your review.');
        return;
    }
    
    const formData = {
        professor: document.getElementById('professorName').value,
        subject: document.getElementById('subjectName').value,
        university: document.getElementById('universityName').value,
        rating: currentRating,
        review: document.getElementById('reviewText').value,
        anonymous: document.getElementById('anonymous').checked
    };
    
    // Simulate form submission
    anime({
        targets: '#reviewForm',
        opacity: [1, 0.5],
        duration: 300,
        complete: function() {
            setTimeout(() => {
                alert('Thank you for your review! It has been submitted for moderation.');
                closeAddReview();
            }, 500);
        }
    });
}

// Navigation Functions
function viewProfessor(professorId) {
    // Store professor ID in localStorage for the professor page
    localStorage.setItem('selectedProfessorId', professorId);
    window.location.href = 'professor.html';
}

// Load More Functionality
document.addEventListener('DOMContentLoaded', function() {
    const loadMoreBtn = document.getElementById('loadMoreBtn');
    if (loadMoreBtn) {
        loadMoreBtn.addEventListener('click', function() {
            // Simulate loading more results
            this.textContent = 'Loading...';
            this.disabled = true;
            
            setTimeout(() => {
                this.textContent = 'Load More';
                this.disabled = false;
                // In a real app, you would load more data here
            }, 1000);
        });
    }
});

// Add smooth scrolling for anchor links
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

// Add loading states and error handling
function showLoading(element) {
    element.innerHTML = '<div class="flex justify-center items-center py-12"><div class="animate-spin rounded-full h-12 w-12 border-b-2 border-gold"></div></div>';
}

function showError(element, message) {
    element.innerHTML = `
        <div class="text-center py-12">
            <div class="text-red-500 text-6xl mb-4">⚠️</div>
            <h3 class="text-xl font-semibold text-gray-900 mb-2">Error</h3>
            <p class="text-gray-600">${message}</p>
        </div>
    `;
}
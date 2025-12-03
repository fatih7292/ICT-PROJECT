// Professor page specific JavaScript
let currentProfessor = null;
let currentRating = 0;
let allReviews = [];
let displayedReviews = [];
let reviewsPerPage = 5;

// Complete professors data
const professorsData = [
    {
        id: 1,
        name: "Dr. Sarah Johnson",
        subject: "Computer Science",
        university: "Stanford University",
        image: "/images/Professor.jpg",
        rating: 4.9,
        reviewCount: 127,
        specialties: ["Artificial Intelligence", "Machine Learning", "Data Science"],
        bio: "Dr. Sarah Johnson is a leading researcher in artificial intelligence with over 15 years of teaching experience. She holds a PhD in Computer Science from MIT and has published numerous papers in top-tier conferences. Her passion for making complex AI concepts accessible to students has earned her consistently high ratings. She believes in hands-on learning and often incorporates real-world projects into her curriculum.",
        reviews: [
            {
                id: 1,
                author: "Alex Thompson",
                avatar: "resources/student-avatars/avatar-1.jpg",
                rating: 5,
                date: "2024-01-15",
                course: "CS101",
                semester: "Fall 2023",
                text: "Dr. Johnson is absolutely amazing! She has this incredible ability to break down complex AI concepts into digestible pieces. Her lectures are engaging, and she always provides real-world examples that make the material click. The projects were challenging but rewarding, and her feedback was always constructive and helpful. I would definitely take another class with her!",
                helpful: 23,
                anonymous: false
            },
            {
                id: 2,
                author: "Maria Garcia",
                avatar: "/images/StudentAvatar.jpg",
                rating: 5,
                date: "2024-01-10",
                course: "CS201",
                semester: "Fall 2023",
                text: "One of the best professors I've had at Stanford. Dr. Johnson's enthusiasm for AI is infectious, and she creates such a positive learning environment. She's always available during office hours and genuinely cares about student success. The coursework is rigorous but fair, and you learn so much practical knowledge.",
                helpful: 18,
                anonymous: false
            },
            {
                id: 3,
                author: "David Kim",
                avatar: "resources/student-avatars/avatar-3.jpg",
                rating: 4,
                date: "2024-01-08",
                course: "CS301",
                semester: "Spring 2023",
                text: "Great professor with deep knowledge of the subject. The only reason I'm giving 4 stars instead of 5 is that the pacing can be quite fast, especially towards the end of the semester. However, if you stay on top of the material and attend office hours, you'll learn a tremendous amount. Her research insights are particularly valuable.",
                helpful: 12,
                anonymous: false
            },
            {
                id: 4,
                author: "Student123",
                avatar: "resources/student-avatars/avatar-4.jpg",
                rating: 5,
                date: "2023-12-20",
                course: "CS101",
                semester: "Fall 2023",
                text: "I was initially intimidated by AI, but Dr. Johnson made it so accessible. Her teaching style is perfect for beginners while still being challenging enough for advanced students. The guest speakers she brought in from industry were fantastic additions to the curriculum.",
                helpful: 8,
                anonymous: true
            },
            {
                id: 5,
                author: "Sarah M",
                avatar: "resources/student-avatars/avatar-5.jpg",
                rating: 5,
                date: "2023-12-15",
                course: "CS201",
                semester: "Fall 2023",
                text: "Absolutely phenomenal professor! Dr. Johnson goes above and beyond for her students. She remembers everyone's name, provides detailed feedback on assignments, and creates such an inclusive classroom environment. Her expertise in machine learning is evident in every lecture.",
                helpful: 15,
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
        specialties: ["Calculus", "Linear Algebra", "Differential Equations"],
        bio: "Prof. Michael Chen is an award-winning mathematician with a gift for making complex mathematical concepts accessible to students of all levels. With over 12 years of teaching experience at MIT, he has developed innovative teaching methods that help students grasp abstract mathematical ideas. His research focuses on applied mathematics and numerical analysis.",
        reviews: [
            {
                id: 1,
                author: "Math_Lover",
                avatar: "resources/student-avatars/avatar-1.jpg",
                rating: 5,
                date: "2024-01-12",
                course: "MATH201",
                semester: "Fall 2023",
                text: "Prof. Chen is exceptional! He explains difficult concepts with clarity and patience. His problem-solving sessions are incredibly helpful, and he always makes sure everyone understands before moving forward.",
                helpful: 15,
                anonymous: true
            },
            {
                id: 2,
                author: "Jennifer Lee",
                avatar: "/images/StudentAvatar.jpg",
                rating: 4,
                date: "2024-01-05",
                course: "MATH301",
                semester: "Fall 2023",
                text: "Great professor but moves through material quickly. Be prepared to study! His office hours are very helpful though.",
                helpful: 10,
                anonymous: false
            },
            {
                id: 3,
                author: "Tom Wilson",
                avatar: "resources/student-avatars/avatar-3.jpg",
                rating: 5,
                date: "2023-12-18",
                course: "MATH101",
                semester: "Fall 2023",
                text: "Prof. Chen made me actually enjoy math! His enthusiasm is contagious and his teaching methods are top-notch.",
                helpful: 20,
                anonymous: false
            }
        ]
    },
    {
        id: 3,
        name: "Dr. Emily Rodriguez",
        subject: "Physics",
        university: "Caltech",
        image: "/images/Physics.jpg",
        rating: 4.8,
        reviewCount: 156,
        specialties: ["Quantum Mechanics", "Particle Physics", "Astrophysics"],
        bio: "Dr. Emily Rodriguez is a brilliant physicist who brings energy and excitement to every lecture. Her groundbreaking research in particle physics has been published in prestigious journals, and she has a remarkable ability to make complex physical phenomena understandable and fascinating. Students consistently praise her engaging teaching style and dedication to their success.",
        reviews: [
            {
                id: 1,
                author: "Physics_Student",
                avatar: "resources/student-avatars/avatar-4.jpg",
                rating: 5,
                date: "2024-01-08",
                course: "PHYS301",
                semester: "Fall 2023",
                text: "Dr. Rodriguez is amazing! Her demonstrations make physics come alive. She's passionate about the subject and it shows in every class.",
                helpful: 31,
                anonymous: false
            },
            {
                id: 2,
                author: "John Smith",
                avatar: "resources/student-avatars/avatar-5.jpg",
                rating: 5,
                date: "2023-12-22",
                course: "PHYS201",
                semester: "Fall 2023",
                text: "Best physics professor I've ever had. Her explanations are crystal clear and she makes difficult concepts easy to understand.",
                helpful: 25,
                anonymous: false
            },
            {
                id: 3,
                author: "Anonymous",
                avatar: "resources/student-avatars/avatar-6.jpg",
                rating: 4,
                date: "2023-12-15",
                course: "PHYS101",
                semester: "Fall 2023",
                text: "Great professor! The only downside is that exams can be quite challenging, but they're fair and test your understanding well.",
                helpful: 18,
                anonymous: true
            }
        ]
    },
    {
        id: 4,
        name: "Prof. David Kim",
        subject: "Chemistry",
        university: "Harvard University",
        image: "/images/ChemistryProfessor.jpg",
        rating: 4.6,
        reviewCount: 98,
        specialties: ["Organic Chemistry", "Biochemistry", "Medicinal Chemistry"],
        bio: "Prof. David Kim is a dedicated teacher with innovative lab techniques and a focus on real-world applications of chemistry. His research in medicinal chemistry has led to several patents, and he brings this practical experience into the classroom. Students appreciate his clear explanations and his ability to relate chemistry to everyday life and medical applications.",
        reviews: [
            {
                id: 1,
                author: "Chem_Major",
                avatar: "resources/student-avatars/avatar-1.jpg",
                rating: 5,
                date: "2024-01-14",
                course: "CHEM201",
                semester: "Fall 2023",
                text: "Prof. Kim makes organic chemistry so much easier to understand. His lab sessions are well-organized and educational.",
                helpful: 22,
                anonymous: false
            },
            {
                id: 2,
                author: "Lisa Chen",
                avatar: "/images/StudentAvatar.jpg",
                rating: 4,
                date: "2024-01-06",
                course: "CHEM301",
                semester: "Fall 2023",
                text: "Very knowledgeable professor. The course is challenging but you learn a lot. His real-world examples are particularly helpful.",
                helpful: 16,
                anonymous: false
            },
            {
                id: 3,
                author: "Mike Johnson",
                avatar: "resources/student-avatars/avatar-3.jpg",
                rating: 5,
                date: "2023-12-20",
                course: "CHEM101",
                semester: "Fall 2023",
                text: "Excellent professor! He's patient, explains things clearly, and is always willing to help during office hours.",
                helpful: 19,
                anonymous: false
            }
        ]
    },
    {
        id: 5,
        name: "Dr. Lisa Thompson",
        subject: "Biology",
        university: "Yale University",
        image: "resources/professor-5.jpg",
        rating: 4.9,
        reviewCount: 203,
        specialties: ["Genetics", "Molecular Biology", "Evolutionary Biology"],
        bio: "Dr. Lisa Thompson is a passionate biologist who inspires students to explore the natural world. Her research in genetics has contributed significantly to our understanding of gene expression and regulation. She is known for her engaging lectures, comprehensive course materials, and genuine care for student learning. Her field trips and lab experiences provide hands-on learning opportunities that students find invaluable.",
        reviews: [
            {
                id: 1,
                author: "Bio_Student",
                avatar: "resources/student-avatars/avatar-4.jpg",
                rating: 5,
                date: "2024-01-16",
                course: "BIO201",
                semester: "Fall 2023",
                text: "Dr. Thompson is incredible! Her passion for biology is inspiring and her teaching methods are excellent. The field trips were amazing!",
                helpful: 35,
                anonymous: false
            },
            {
                id: 2,
                author: "Rachel Green",
                avatar: "resources/student-avatars/avatar-5.jpg",
                rating: 5,
                date: "2024-01-09",
                course: "BIO301",
                semester: "Fall 2023",
                text: "Best biology professor at Yale! She makes complex genetic concepts easy to understand and her enthusiasm is contagious.",
                helpful: 28,
                anonymous: false
            },
            {
                id: 3,
                author: "Student456",
                avatar: "resources/student-avatars/avatar-6.jpg",
                rating: 5,
                date: "2023-12-28",
                course: "BIO101",
                semester: "Fall 2023",
                text: "Dr. Thompson's class changed my perspective on biology. Her lectures are engaging and the lab work is fascinating.",
                helpful: 24,
                anonymous: true
            },
            {
                id: 4,
                author: "Kevin Brown",
                avatar: "resources/student-avatars/avatar-1.jpg",
                rating: 4,
                date: "2023-12-18",
                course: "BIO201",
                semester: "Fall 2023",
                text: "Excellent professor! The workload is heavy but manageable. You'll learn a ton in her class.",
                helpful: 17,
                anonymous: false
            }
        ]
    },
    {
        id: 6,
        name: "Prof. James Wilson",
        subject: "English Literature",
        university: "Oxford University",
        image: "resources/professor-6.jpg",
        rating: 4.5,
        reviewCount: 74,
        specialties: ["Shakespeare", "Modern Literature", "Literary Theory"],
        bio: "Prof. James Wilson is a literary scholar with a talent for making classic literature relevant to today's students. His deep knowledge of Shakespeare and modern literature, combined with his engaging teaching style, makes his classes both educational and entertaining. He encourages critical thinking and lively discussions, creating an intellectually stimulating environment where students feel comfortable sharing their interpretations.",
        reviews: [
            {
                id: 1,
                author: "Lit_Lover",
                avatar: "/images/StudentAvatar.jpg",
                rating: 5,
                date: "2024-01-11",
                course: "ENG201",
                semester: "Fall 2023",
                text: "Prof. Wilson brings Shakespeare to life! His lectures are fascinating and he encourages great discussions in class.",
                helpful: 21,
                anonymous: false
            },
            {
                id: 2,
                author: "Emma Watson",
                avatar: "resources/student-avatars/avatar-3.jpg",
                rating: 4,
                date: "2024-01-03",
                course: "ENG301",
                semester: "Fall 2023",
                text: "Very knowledgeable professor. His analysis of literature is insightful. The reading list is extensive but worthwhile.",
                helpful: 14,
                anonymous: false
            },
            {
                id: 3,
                author: "Anonymous",
                avatar: "resources/student-avatars/avatar-4.jpg",
                rating: 5,
                date: "2023-12-19",
                course: "ENG101",
                semester: "Fall 2023",
                text: "Prof. Wilson made me appreciate literature in a whole new way. His passion for the subject is evident in every class.",
                helpful: 18,
                anonymous: true
            }
        ]
    }
];

// Initialize professor page
document.addEventListener('DOMContentLoaded', function() {
    initializeProfessorPage();
});

function initializeProfessorPage() {
    // Get professor ID from localStorage
    const professorId = localStorage.getItem('selectedProfessorId');
    if (!professorId) {
        // Redirect to home if no professor ID
        window.location.href = 'index.html';
        return;
    }

    // Load professor data
    loadProfessorData(parseInt(professorId));
    
    // Initialize review form
    initializeReviewForm();
    
    // Initialize sort functionality
    document.getElementById('sortReviews').addEventListener('change', handleSortReviews);
    
    // Initialize load more button
    document.getElementById('loadMoreReviews').addEventListener('click', loadMoreReviews);
}

function loadProfessorData(professorId) {
    currentProfessor = professorsData.find(p => p.id === professorId);
    
    if (!currentProfessor) {
        // If professor not found, redirect to home
        window.location.href = 'index.html';
        return;
    }

    // Populate professor information
    populateProfessorInfo();
    
    // Initialize reviews
    allReviews = [...currentProfessor.reviews];
    displayedReviews = [];
    
    // Display initial reviews
    displayReviews();
    
    // Initialize rating chart
    initializeRatingChart();
    
    // Load related professors
    loadRelatedProfessors();
}

function populateProfessorInfo() {
    document.getElementById('professorImage').src = currentProfessor.image;
    document.getElementById('professorImage').alt = currentProfessor.name;
    document.getElementById('professorName').textContent = currentProfessor.name;
    document.getElementById('professorSubject').textContent = currentProfessor.subject;
    document.getElementById('professorUniversity').textContent = currentProfessor.university;
    document.getElementById('professorBio').textContent = currentProfessor.bio;
    
    // Rating
    const ratingElement = document.getElementById('professorRating');
    ratingElement.innerHTML = generateStars(currentProfessor.rating);
    document.getElementById('ratingValue').textContent = currentProfessor.rating;
    document.getElementById('reviewCount').textContent = `${currentProfessor.reviewCount} reviews`;
    
    // Statistics
    document.getElementById('overallRating').textContent = currentProfessor.rating;
    document.getElementById('totalReviews').textContent = currentProfessor.reviewCount;
    
    // Specialties
    const specialtiesContainer = document.getElementById('professorSpecialties');
    specialtiesContainer.innerHTML = currentProfessor.specialties.map(spec => 
        `<span class="bg-blue-100 text-blue-800 text-sm px-3 py-1 rounded-full">${spec}</span>`
    ).join('');
    
    // Modal information
    document.getElementById('modalProfessorImage').src = currentProfessor.image;
    document.getElementById('modalProfessorName').textContent = currentProfessor.name;
    document.getElementById('modalProfessorSubject').textContent = currentProfessor.subject;
}

function generateStars(rating) {
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 >= 0.5;
    const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);
    
    let stars = '';
    
    for (let i = 0; i < fullStars; i++) {
        stars += '<span class="text-gold">★</span>';
    }
    
    if (hasHalfStar) {
        stars += '<span class="text-gold">☆</span>';
    }
    
    for (let i = 0; i < emptyStars; i++) {
        stars += '<span class="text-gray-300">★</span>';
    }
    
    return stars;
}

function displayReviews(startIndex = 0) {
    const container = document.getElementById('reviewsContainer');
    const reviewsToShow = allReviews.slice(startIndex, startIndex + reviewsPerPage);
    
    if (startIndex === 0) {
        container.innerHTML = '';
        displayedReviews = [];
    }
    
    displayedReviews.push(...reviewsToShow);
    
    reviewsToShow.forEach(review => {
        const reviewElement = createReviewElement(review);
        container.appendChild(reviewElement);
    });
    
    // Show/hide load more button
    const loadMoreBtn = document.getElementById('loadMoreReviews');
    if (displayedReviews.length >= allReviews.length) {
        loadMoreBtn.style.display = 'none';
    } else {
        loadMoreBtn.style.display = 'block';
    }
}

function createReviewElement(review) {
    const div = document.createElement('div');
    div.className = 'review-card bg-white rounded-2xl p-6 shadow-lg fade-in';
    
    div.innerHTML = `
        <div class="flex items-start gap-4">
            <img src="${review.avatar}" alt="${review.author}" class="w-12 h-12 rounded-full object-cover flex-shrink-0">
            <div class="flex-1">
                <div class="flex items-center justify-between mb-2">
                    <div>
                        <h3 class="font-semibold text-gray-900">${review.anonymous ? 'Anonymous' : review.author}</h3>
                        <div class="flex items-center gap-2 text-sm text-gray-600">
                            <span>${review.course}</span>
                            <span>•</span>
                            <span>${review.semester}</span>
                            <span>•</span>
                            <span>${formatDate(review.date)}</span>
                        </div>
                    </div>
                    <div class="flex items-center">
                        <div class="rating-stars text-lg mr-2">
                            ${generateStars(review.rating)}
                        </div>
                        <span class="text-gray-700 font-semibold">${review.rating}</span>
                    </div>
                </div>
                <p class="text-gray-700 leading-relaxed mb-4">${review.text}</p>
                <div class="flex items-center gap-4">
                    <button onclick="markHelpful(${review.id})" class="helpful-btn flex items-center gap-2 px-3 py-1 rounded-full text-sm border border-gray-300 hover:border-success transition-colors">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21H9.737a2 2 0 01-1.789-1.106l-3.5-7A2 2 0 016.236 10H11V5a2 2 0 114 0v5z"></path>
                        </svg>
                        Helpful (${review.helpful})
                    </button>
                    <button onclick="reportReview(${review.id})" class="text-gray-500 hover:text-red-500 text-sm transition-colors">
                        Report
                    </button>
                </div>
            </div>
        </div>
    `;
    
    return div;
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
    });
}

function handleSortReviews() {
    const sortBy = document.getElementById('sortReviews').value;
    
    switch (sortBy) {
        case 'newest':
            allReviews.sort((a, b) => new Date(b.date) - new Date(a.date));
            break;
        case 'oldest':
            allReviews.sort((a, b) => new Date(a.date) - new Date(b.date));
            break;
        case 'highest':
            allReviews.sort((a, b) => b.rating - a.rating);
            break;
        case 'lowest':
            allReviews.sort((a, b) => a.rating - b.rating);
            break;
        case 'helpful':
            allReviews.sort((a, b) => b.helpful - a.helpful);
            break;
    }
    
    displayReviews();
}

function loadMoreReviews() {
    displayReviews(displayedReviews.length);
}

function initializeRatingChart() {
    const chart = echarts.init(document.getElementById('ratingChart'));
    
    // Calculate rating distribution
    const ratingCounts = [0, 0, 0, 0, 0];
    allReviews.forEach(review => {
        ratingCounts[review.rating - 1]++;
    });
    
    const option = {
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            type: 'category',
            data: ['1 Star', '2 Stars', '3 Stars', '4 Stars', '5 Stars'],
            axisLabel: {
                color: '#6B7280'
            }
        },
        yAxis: {
            type: 'value',
            axisLabel: {
                color: '#6B7280'
            }
        },
        series: [{
            name: 'Number of Reviews',
            type: 'bar',
            data: ratingCounts,
            itemStyle: {
                color: '#d97706'
            },
            barWidth: '60%'
        }]
    };
    
    chart.setOption(option);
    
    // Make chart responsive
    window.addEventListener('resize', function() {
        chart.resize();
    });
}

function loadRelatedProfessors() {
    const container = document.getElementById('relatedProfessors');
    
    // Get other professors from the same subject or university
    const relatedProfs = professorsData
        .filter(p => p.id !== currentProfessor.id)
        .slice(0, 3);
    
    container.innerHTML = relatedProfs.map(prof => `
        <div class="flex items-center justify-between p-3 bg-soft-gray rounded-lg cursor-pointer hover:bg-gray-200 transition-colors" onclick="viewProfessor(${prof.id})">
            <div>
                <div class="font-semibold text-sm text-gray-900">${prof.name}</div>
                <div class="text-xs text-gray-600">${prof.subject}</div>
            </div>
            <div class="text-right">
                <div class="rating-stars text-sm">${generateStars(prof.rating)}</div>
                <div class="text-xs text-gray-600">${prof.rating}</div>
            </div>
        </div>
    `).join('');
}

function viewProfessor(professorId) {
    localStorage.setItem('selectedProfessorId', professorId);
    window.location.reload();
}

// Review interaction functions
function markHelpful(reviewId) {
    const review = allReviews.find(r => r.id === reviewId);
    if (review) {
        review.helpful++;
        // Refresh the display
        displayReviews();
    }
}

function reportReview(reviewId) {
    if (confirm('Are you sure you want to report this review?')) {
        alert('Thank you for your report. We will review this review shortly.');
    }
}

function shareProfessor() {
    if (navigator.share) {
        navigator.share({
            title: `${currentProfessor.name} - Feedback System`,
            text: `Check out reviews for ${currentProfessor.name} on Feedback System`,
            url: window.location.href
        });
    } else {
        // Fallback for browsers that don't support Web Share API
        navigator.clipboard.writeText(window.location.href);
        alert('Link copied to clipboard!');
    }
}

// Modal functions
function showAddReview() {
    const modal = document.getElementById('addReviewModal');
    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

function closeAddReview() {
    const modal = document.getElementById('addReviewModal');
    modal.classList.add('hidden');
    document.body.style.overflow = 'auto';
    resetReviewForm();
}

function initializeReviewForm() {
    const ratingStars = document.querySelectorAll('.star');
    const reviewText = document.getElementById('reviewText');
    
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
    
    if (reviewText) {
        reviewText.addEventListener('input', function() {
            const count = this.value.length;
            document.getElementById('charCount').textContent = count;
            
            if (count > 1000) {
                this.value = this.value.substring(0, 1000);
                document.getElementById('charCount').textContent = 1000;
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
        course: document.getElementById('courseName').value,
        semester: document.getElementById('semester').value,
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
                
                // Add the new review to the list
                const newReview = {
                    id: allReviews.length + 1,
                    author: formData.anonymous ? 'Anonymous' : 'You',
                    avatar: 'resources/student-avatars/avatar-1.jpg',
                    rating: formData.rating,
                    date: new Date().toISOString().split('T')[0],
                    course: formData.course,
                    semester: formData.semester,
                    text: formData.review,
                    helpful: 0,
                    anonymous: formData.anonymous
                };
                
                allReviews.unshift(newReview);
                displayReviews();
            }, 500);
        }
    });
}
// Reddot Events Data processing utilities for CSV data
class ReddotDashboardData {
    constructor() {
        this.platforms = [];
        this.hashtags = [];
        this.competitors = [];
        this.processedData = {};
    }

    // Parse CSV data from the Reddot file
    async loadData() {
        // Platform data from Reddot CSV with actual Google Docs links and platform URLs
        this.platforms = [
            { sno: '', platform: 'Website', pastStatus: 'Already in Place', committed: '--', drafted: '--', published: '--', contentCreated: '', platformLink: '', category: 'Digital Identity', primaryContent: '' },
            { sno: 1, platform: 'Website- blogs', pastStatus: 'Not Active', committed: 50, drafted: 10, published: 0, contentCreated: 'https://docs.google.com/document/d/1KLdqfleDIyuAH-xdZYCqPlEVqqqQahdWHeNxeGhQ4mI/edit?usp=drive_link', platformLink: '', category: 'Professional Writing', primaryContent: 'Long-form Articles, Thought Leadership' },
            { sno: 2, platform: 'Website Downloadable', pastStatus: 'Not Active', committed: 10, drafted: 1, published: 0, contentCreated: 'https://docs.google.com/document/d/1wNXUmUtpAIFkJKSsigESAWQ3iyfiBaMO-upq6PHseRg/edit?usp=drive_link', platformLink: '', category: 'Informational Content', primaryContent: 'Infographics, Product related, knowledge articles' },
            { sno: 3, platform: 'Google Business', pastStatus: 'Not Active', committed: 100, drafted: 11, published: 0, contentCreated: 'https://docs.google.com/document/d/13CfHO2BSMQ-hIZ-Ix05vzKa6c02Cq1zoxN4TlquH7Sw/edit?usp=drive_link', platformLink: '', category: 'Local Business', primaryContent: 'Business Info, Reviews, Local Posts' },
            { sno: 4, platform: 'Linkedin', pastStatus: 'Not Active', committed: 45, drafted: 10, published: 0, contentCreated: 'https://docs.google.com/document/d/1nMDbcpbB0bQ90P8guHZE3iy6m827Jcve4DqV3uJYWFU/edit?usp=drive_link', platformLink: 'https://www.linkedin.com/company/red-dot-events-exhibitions-sp-llc/', category: 'Professional Network', primaryContent: 'Articles, Company Updates, Industry News' },
            { sno: 5, platform: 'YouTube', pastStatus: 'Not Active', committed: 5, drafted: 1, published: 0, contentCreated: 'https://drive.google.com/drive/folders/1VjLK1PtsG1A4cdGsDmRWRdNkr3AJA2Md?usp=drive_link', platformLink: '', category: 'Long-Form Video', primaryContent: 'Long Videos, Tutorials, Vlogs' },
            { sno: 6, platform: 'Tiktok', pastStatus: 'Not Active', committed: 10, drafted: 1, published: 0, contentCreated: '', platformLink: '', category: 'Short-Form Video', primaryContent: 'Short Videos, Challenges, Trends' },
            { sno: 7, platform: 'Instagram', pastStatus: 'Active', committed: 180, drafted: 45, published: 0, contentCreated: 'https://docs.google.com/document/d/1wbCr8wavITL10BnEAdURYDKzqgsIEbPnoyo6vjnD9co/edit?usp=drive_link', platformLink: 'https://www.instagram.com/reddot_event/', category: 'Visual Content', primaryContent: 'Images, Stories, Reels, IGTV' },
            { sno: 8, platform: 'PinInterest', pastStatus: 'Active', committed: 180, drafted: 0, published: 1, contentCreated: 'https://docs.google.com/document/d/1qmdzoOdBIFu-ZKsmVfg85ugij4isTlN7rzeMRp3pFOU/edit?usp=drive_link', platformLink: 'https://www.pinterest.com/reddoteventssocial/', category: 'Visual Content', primaryContent: 'Infographics, Product Images, Boards' },
            { sno: 9, platform: 'X (Twitter)', pastStatus: 'Active', committed: 180, drafted: 10, published: 1, contentCreated: 'https://docs.google.com/document/d/106-J7VxbGOcmcUYL32L4Wx9Cefk8FawMA0Vi9rbHITI/edit?usp=drive_link', platformLink: 'https://x.com/EventsRedd60567', category: 'Real-Time Social', primaryContent: 'Real-time Updates, News, Discussions' },
            { sno: 10, platform: 'Facebook', pastStatus: 'Active', committed: 180, drafted: 10, published: 0, contentCreated: 'https://docs.google.com/document/d/1cw5TJhTsuIbNSEkMYGp6xrhHBTPQi6J1QNGKrE_97fU/edit?usp=drive_link', platformLink: 'https://www.facebook.com/people/Red-Dot-Events/61560412568254/', category: 'Social Community', primaryContent: 'Mixed Content, Community Posts, Events' },
            { sno: 11, platform: 'Medium', pastStatus: 'Active', committed: 30, drafted: 0, published: 2, contentCreated: 'https://docs.google.com/document/d/1zxVTTTxG3-M5NIQJwElBlmD9kusruLawBJHvpsc8a5E/edit?usp=drive_link', platformLink: 'https://medium.com/@reddotevents.social', category: 'Professional Writing', primaryContent: 'Long-form Articles, Thought Leadership' },
            { sno: 12, platform: 'Threads', pastStatus: 'Not Active', committed: 30, drafted: 0, published: 0, contentCreated: 'https://docs.google.com/document/d/16rUK1zYdRsW2OcvCpcxIHyYNfF2dPL9fVIvoUkm_pIw/edit?usp=drive_link', platformLink: 'via Instagram', category: 'Micro-Blogging', primaryContent: 'Short Posts, Real-time Updates' },
            { sno: 13, platform: 'Tumblr', pastStatus: 'Active', committed: 30, drafted: 10, published: 1, contentCreated: '', platformLink: 'https://www.tumblr.com/blog/reddotevents', category: 'Creative Blogging', primaryContent: 'Creative Content, Visual Stories, Blog Posts' }
        ];

        // Sample of hashtag data for Events industry
        this.hashtags = [
            { hashtag: '#ReddotEvents', category: 'Brand Events', usageContext: 'Brand recognition posts, company events', platformSuitability: 'All platforms', popularityScore: 9, bestPostingTime: 'Business hours (9 AM - 6 PM GMT)' },
            { hashtag: '#EventPlanning', category: 'Core Events', usageContext: 'Event planning tips, behind-the-scenes content', platformSuitability: 'All platforms', popularityScore: 10, bestPostingTime: 'Peak hours (9-11 AM, 7-9 PM GMT)' },
            { hashtag: '#CorporateEvents', category: 'Core Events', usageContext: 'B2B event content, corporate partnerships', platformSuitability: 'LinkedIn, Twitter, Facebook', popularityScore: 8, bestPostingTime: 'Business hours (9 AM - 6 PM GMT)' },
            { hashtag: '#EventDesign', category: 'Creative Events', usageContext: 'Visual showcases, design inspiration', platformSuitability: 'Instagram, Pinterest', popularityScore: 9, bestPostingTime: 'Evening (6-10 PM GMT)' },
            { hashtag: '#EventManagement', category: 'Professional Events', usageContext: 'Industry expertise, thought leadership', platformSuitability: 'LinkedIn, Medium', popularityScore: 8, bestPostingTime: 'Business hours (9 AM - 6 PM GMT)' },
            { hashtag: '#WeddingPlanning', category: 'Personal Events', usageContext: 'Wedding showcases, client testimonials', platformSuitability: 'Instagram, Facebook, Pinterest', popularityScore: 10, bestPostingTime: 'Weekends' },
            { hashtag: '#PrivateEvents', category: 'Personal Events', usageContext: 'Intimate gatherings, exclusive events', platformSuitability: 'Instagram, Facebook', popularityScore: 7, bestPostingTime: 'Evening (6-10 PM GMT)' },
            { hashtag: '#EventProduction', category: 'Professional Events', usageContext: 'Technical setup, behind-the-scenes', platformSuitability: 'LinkedIn, YouTube', popularityScore: 6, bestPostingTime: 'Business hours (9 AM - 6 PM GMT)' },
            { hashtag: '#PartyPlanning', category: 'Personal Events', usageContext: 'Fun celebrations, party inspiration', platformSuitability: 'Instagram, TikTok, Facebook', popularityScore: 8, bestPostingTime: 'Weekends' },
            { hashtag: '#EventDecor', category: 'Creative Events', usageContext: 'Decoration showcases, trends', platformSuitability: 'Instagram, Pinterest', popularityScore: 9, bestPostingTime: 'Evening (6-10 PM GMT)' },
            { hashtag: '#EventVenue', category: 'Professional Events', usageContext: 'Venue showcases, location features', platformSuitability: 'All platforms', popularityScore: 7, bestPostingTime: 'Business hours (9 AM - 6 PM GMT)' },
            { hashtag: '#EventCatering', category: 'Service Events', usageContext: 'Food presentations, catering services', platformSuitability: 'Instagram, Facebook', popularityScore: 8, bestPostingTime: 'Peak hours (9-11 AM, 7-9 PM GMT)' },
            { hashtag: '#EventPhotography', category: 'Creative Events', usageContext: 'Photo showcases, event memories', platformSuitability: 'Instagram, Pinterest', popularityScore: 9, bestPostingTime: 'Evening (6-10 PM GMT)' },
            { hashtag: '#EventMarketing', category: 'Professional Events', usageContext: 'Marketing strategies, promotion tips', platformSuitability: 'LinkedIn, Twitter', popularityScore: 6, bestPostingTime: 'Business hours (9 AM - 6 PM GMT)' },
            { hashtag: '#EventTech', category: 'Technology Events', usageContext: 'Tech integration, modern solutions', platformSuitability: 'LinkedIn, Twitter, YouTube', popularityScore: 7, bestPostingTime: 'Business hours (9 AM - 6 PM GMT)' },
            { hashtag: '#LuxuryEvents', category: 'Premium Events', usageContext: 'High-end events, luxury experiences', platformSuitability: 'Instagram, LinkedIn', popularityScore: 8, bestPostingTime: 'Evening (6-10 PM GMT)' },
            { hashtag: '#EventInnovation', category: 'Creative Events', usageContext: 'New ideas, creative solutions', platformSuitability: 'LinkedIn, Medium', popularityScore: 7, bestPostingTime: 'Business hours (9 AM - 6 PM GMT)' },
            { hashtag: '#SustainableEvents', category: 'Eco Events', usageContext: 'Eco-friendly practices, green events', platformSuitability: 'All platforms', popularityScore: 8, bestPostingTime: 'Peak hours (9-11 AM, 7-9 PM GMT)' },
            { hashtag: '#EventNetworking', category: 'Professional Events', usageContext: 'Networking opportunities, connections', platformSuitability: 'LinkedIn, Twitter', popularityScore: 9, bestPostingTime: 'Business hours (9 AM - 6 PM GMT)' },
            { hashtag: '#EventSuccess', category: 'Brand Events', usageContext: 'Success stories, testimonials', platformSuitability: 'All platforms', popularityScore: 10, bestPostingTime: 'Business hours (9 AM - 6 PM GMT)' }
        ];

        // Competitors data for Events industry
        this.competitors = [
            { rank: 1, name: 'Elite Events Co.', website: '' },
            { rank: 2, name: 'Premier Event Solutions', website: '' },
            { rank: 3, name: 'Creative Events Hub', website: '' },
            { rank: 4, name: 'Luxury Event Planners', website: '' },
            { rank: 5, name: 'Corporate Events Pro', website: '' },
            { rank: 6, name: 'Wedding Dreams Events', website: '' },
            { rank: 7, name: 'Event Masters Dubai', website: '' },
            { rank: 8, name: 'Platinum Events', website: '' },
            { rank: 9, name: 'Signature Events', website: '' },
            { rank: 10, name: 'Dream Event Planners', website: '' }
        ];

        this.processAnalytics();
    }

    processAnalytics() {
        // Calculate platform statistics
        const activePlatforms = this.platforms.filter(p => p.pastStatus === 'Active').length;
        const inactivePlatforms = this.platforms.filter(p => p.pastStatus === 'Not Active').length;
        const alreadyInPlace = this.platforms.filter(p => p.pastStatus === 'Already in Place').length;
        
        // Calculate content metrics - Updated totals from platform data
        const totalCommitted = this.platforms.reduce((sum, p) => {
            return sum + (typeof p.committed === 'number' ? p.committed : 0);
        }, 0);
        const totalDrafted = this.platforms.reduce((sum, p) => {
            return sum + (typeof p.drafted === 'number' ? p.drafted : 0);
        }, 0);
        
        // Calculate hashtag analytics
        const categoryBreakdown = {};
        this.hashtags.forEach(h => {
            if (!categoryBreakdown[h.category]) {
                categoryBreakdown[h.category] = { count: 0, avgScore: 0, totalScore: 0 };
            }
            categoryBreakdown[h.category].count++;
            categoryBreakdown[h.category].totalScore += h.popularityScore;
        });

        // Calculate average scores
        Object.keys(categoryBreakdown).forEach(cat => {
            categoryBreakdown[cat].avgScore = Math.round(
                categoryBreakdown[cat].totalScore / categoryBreakdown[cat].count * 10
            ) / 10;
        });

        // Get top hashtags (score 8-10)
        const topHashtags = this.hashtags
            .filter(h => h.popularityScore >= 8)
            .sort((a, b) => b.popularityScore - a.popularityScore);

        // Process platform categories
        const platformCategories = {};
        this.platforms.forEach(p => {
            if (p.category && p.category !== '') {
                if (!platformCategories[p.category]) {
                    platformCategories[p.category] = {
                        count: 0,
                        active: 0,
                        inactive: 0,
                        totalCommitted: 0
                    };
                }
                platformCategories[p.category].count++;
                if (p.pastStatus === 'Active') platformCategories[p.category].active++;
                else if (p.pastStatus === 'Not Active') platformCategories[p.category].inactive++;
                
                if (typeof p.committed === 'number') {
                    platformCategories[p.category].totalCommitted += p.committed;
                }
            }
        });

        this.processedData = {
            platformStats: {
                active: activePlatforms,
                inactive: inactivePlatforms,
                alreadyInPlace: alreadyInPlace,
                total: 13 // Total Reddot platforms (including Tumblr)
            },
            contentMetrics: {
                totalCommitted,
                totalDrafted,
                completionRate: totalCommitted > 0 ? Math.round((totalDrafted / totalCommitted) * 100) : 0
            },
            hashtagAnalytics: {
                categoryBreakdown,
                topHashtags,
                totalCategories: Object.keys(categoryBreakdown).length
            },
            platformCategories,
            competitors: this.competitors
        };
    }

    // Helper method to format clickable links
    formatContentLink(contentCreated, platformName) {
        if (!contentCreated) return '';
        
        // Check if it's a Google Docs link
        if (contentCreated.startsWith('https://docs.google.com/')) {
            return `<a href="${contentCreated}" target="_blank" class="content-link">📄 View Content Plan</a>`;
        }
        
        // Check if it's a Google Drive link
        if (contentCreated.startsWith('https://drive.google.com/')) {
            return `<a href="${contentCreated}" target="_blank" class="content-link">📁 View Content Folder</a>`;
        }
        
        return contentCreated;
    }

    // Getter methods for dashboard components
    getPlatformStats() {
        return this.processedData.platformStats;
    }

    getContentMetrics() {
        return this.processedData.contentMetrics;
    }

    getHashtagAnalytics() {
        return this.processedData.hashtagAnalytics;
    }

    getPlatformCategories() {
        return this.processedData.platformCategories;
    }

    getTopHashtags(limit = 10) {
        return this.processedData.hashtagAnalytics.topHashtags.slice(0, limit);
    }

    getPlatformsByStatus(status) {
        return this.platforms.filter(p => p.pastStatus === status);
    }

    getInactivePlatformsWithPotential() {
        return this.platforms
            .filter(p => p.pastStatus === 'Not Active' && p.contentCreated !== '')
            .sort((a, b) => (b.committed || 0) - (a.committed || 0));
    }

    getHashtagsByCategory(category) {
        return this.hashtags.filter(h => h.category === category);
    }

    searchHashtags(query) {
        const lowerQuery = query.toLowerCase();
        return this.hashtags.filter(h => 
            h.hashtag.toLowerCase().includes(lowerQuery) ||
            h.category.toLowerCase().includes(lowerQuery) ||
            h.usageContext.toLowerCase().includes(lowerQuery)
        );
    }

    searchPlatforms(query) {
        const lowerQuery = query.toLowerCase();
        return this.platforms.filter(p => 
            p.platform.toLowerCase().includes(lowerQuery) ||
            p.category.toLowerCase().includes(lowerQuery) ||
            p.primaryContent.toLowerCase().includes(lowerQuery)
        );
    }
}

// Initialize Reddot data instance
const reddotDashboardData = new ReddotDashboardData();
reddotDashboardData.loadData();
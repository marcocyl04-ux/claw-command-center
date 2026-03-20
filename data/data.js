// Data layer for Claw Command Center
const DataLayer = {
    cache: {},
    
    async fetchJSON(filename) {
        try {
            const response = await fetch(`data/${filename}.json?t=${Date.now()}`);
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error(`Failed to fetch ${filename}:`, error);
            return null;
        }
    },
    
    async getActivity(limit = 10) {
        const data = await this.fetchJSON('activity');
        if (!data) return [];
        return data.slice(0, limit);
    },
    
    async getPredictions(filters = {}) {
        const data = await this.fetchJSON('predictions');
        if (!data) return [];
        
        let filtered = data;
        
        if (filters.outcome) {
            filtered = filtered.filter(p => p.outcome === filters.outcome);
        }
        if (filters.direction) {
            filtered = filtered.filter(p => p.direction === filters.direction);
        }
        if (filters.search) {
            const search = filters.search.toLowerCase();
            filtered = filtered.filter(p => 
                p.market.toLowerCase().includes(search) ||
                p.reasoning.toLowerCase().includes(search)
            );
        }
        
        return filtered;
    },
    
    async getFiles() {
        const data = await this.fetchJSON('files');
        if (!data) return { files: [], lastScan: null };
        return data;
    },
    
    getStats(predictions) {
        const total = predictions.length;
        const validated = predictions.filter(p => p.outcome === 'validated').length;
        const failed = predictions.filter(p => p.outcome === 'failed').length;
        const pending = predictions.filter(p => p.outcome === 'pending').length;
        
        const validatedPredictions = predictions.filter(p => p.outcome === 'validated');
        const avgEdge = validatedPredictions.length > 0 
            ? validatedPredictions.reduce((sum, p) => sum + (p.edge || 0), 0) / validatedPredictions.length 
            : 0;
        
        return {
            total,
            validated,
            failed,
            pending,
            winRate: total > 0 ? (validated / (validated + failed) * 100).toFixed(1) : 0,
            avgEdge: avgEdge.toFixed(1)
        };
    }
};

// Export for use in dashboard
window.DataLayer = DataLayer;

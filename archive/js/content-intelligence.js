/**
 * Content Intelligence Module
 * Transforms raw data into actionable insights
 */

const ContentIntelligence = {
  // Analyze predictions and generate insights
  analyzePredictions(predictions) {
    const validated = predictions.filter(p => p.outcome === 'validated');
    const failed = predictions.filter(p => p.outcome === 'failed');
    const pending = predictions.filter(p => p.outcome === 'pending');
    
    // Confidence calibration analysis
    const byConfidence = {};
    predictions.forEach(p => {
      const bucket = Math.floor(p.predicted / 10) * 10;
      if (!byConfidence[bucket]) byConfidence[bucket] = { total: 0, correct: 0 };
      byConfidence[bucket].total++;
      if (p.outcome === 'validated') byConfidence[bucket].correct++;
    });
    
    // Find over/under confidence
    const calibrationIssues = [];
    Object.entries(byConfidence).forEach(([bucket, data]) => {
      if (data.total < 3) return;
      const actualRate = data.correct / data.total;
      const expectedRate = parseInt(bucket) / 100;
      const diff = actualRate - expectedRate;
      
      if (diff < -0.15) {
        calibrationIssues.push({
          range: `${bucket}-${parseInt(bucket)+10}%`,
          issue: 'overconfident',
          actual: Math.round(actualRate * 100),
          expected: parseInt(bucket)
        });
      } else if (diff > 0.15) {
        calibrationIssues.push({
          range: `${bucket}-${parseInt(bucket)+10}%`,
          issue: 'underconfident',
          actual: Math.round(actualRate * 100),
          expected: parseInt(bucket)
        });
      }
    });
    
    // Pattern detection in failures
    const failurePatterns = this.detectFailurePatterns(failed);
    
    // Edge opportunities
    const edges = this.identifyEdges(predictions);
    
    return {
      summary: {
        total: predictions.length,
        validated: validated.length,
        failed: failed.length,
        pending: pending.length,
        winRate: Math.round((validated.length / (validated.length + failed.length)) * 100) || 0
      },
      calibrationIssues,
      failurePatterns,
      edges,
      interventions: this.generateInterventions(predictions, calibrationIssues, failurePatterns)
    };
  },
  
  detectFailurePatterns(failures) {
    const patterns = [];
    
    // Check for weather type patterns
    const weatherTypes = {};
    failures.forEach(f => {
      const type = f.market.includes('Rain') ? 'rain' :
                   f.market.includes('Temp') ? 'temp' :
                   f.market.includes('Snow') ? 'snow' :
                   f.market.includes('Humidity') ? 'humidity' : 'other';
      if (!weatherTypes[type]) weatherTypes[type] = [];
      weatherTypes[type].push(f);
    });
    
    Object.entries(weatherTypes).forEach(([type, fails]) => {
      if (fails.length >= 2) {
        patterns.push({
          type: 'weather',
          category: type,
          count: fails.length,
          insight: this.getWeatherInsight(type, fails)
        });
      }
    });
    
    // Check for timing patterns
    const timingFails = failures.filter(f => 
      f.lesson && (f.lesson.includes('hour') || f.lesson.includes('early') || f.lesson.includes('late'))
    );
    if (timingFails.length >= 2) {
      patterns.push({
        type: 'timing',
        count: timingFails.length,
        insight: 'Timing errors are a recurring failure mode. Weight real-time data higher than historical patterns.'
      });
    }
    
    return patterns;
  },
  
  getWeatherInsight(type, fails) {
    const insights = {
      rain: 'Rain predictions failing — cloud formation timing is harder than expected.',
      temp: 'Temperature predictions failing — microclimate effects underestimated.',
      snow: 'Snow predictions working well — keep current approach.',
      humidity: 'Humidity predictions need refinement — coastal sensor weighting off.'
    };
    return insights[type] || `${type} predictions need attention.`;
  },
  
  identifyEdges(predictions) {
    const edges = [];
    
    // Find markets where Claw consistently beats market odds
    const byMarket = {};
    predictions.forEach(p => {
      const baseName = p.market.replace(/\s+(March|April|May)\s+\d+/, '');
      if (!byMarket[baseName]) byMarket[baseName] = [];
      byMarket[baseName].push(p);
    });
    
    Object.entries(byMarket).forEach(([market, preds]) => {
      if (preds.length < 3) return;
      const validated = preds.filter(p => p.outcome === 'validated').length;
      const rate = validated / preds.length;
      
      if (rate >= 0.7) {
        edges.push({
          market,
          confidence: Math.round(rate * 100),
          sampleSize: preds.length,
          type: 'validated_edge'
        });
      }
    });
    
    return edges;
  },
  
  generateInterventions(predictions, calibrationIssues, failurePatterns) {
    const interventions = [];
    
    // Calibration interventions
    calibrationIssues.forEach(issue => {
      if (issue.issue === 'overconfident') {
        interventions.push({
          priority: 'high',
          type: 'calibration',
          message: `You're overconfident at ${issue.range}. Actual: ${issue.actual}%, Predicted: ${issue.expected}%. Reduce confidence in this range.`,
          action: 'Review 60-70% predictions before making them'
        });
      }
    });
    
    // Pattern interventions
    failurePatterns.forEach(pattern => {
      if (pattern.type === 'timing') {
        interventions.push({
          priority: 'high',
          type: 'pattern',
          message: pattern.insight,
          action: 'Add real-time data weighting to prediction model'
        });
      }
    });
    
    // Pending position alerts
    const pending = predictions.filter(p => p.outcome === 'pending');
    if (pending.length > 0) {
      const highConfidencePending = pending.filter(p => p.predicted >= 80);
      if (highConfidencePending.length > 0) {
        interventions.push({
          priority: 'medium',
          type: 'position',
          message: `${highConfidencePending.length} high-confidence positions pending resolution`,
          action: 'Monitor for resolution scoring'
        });
      }
    }
    
    // Edge deployment
    const edges = this.identifyEdges(predictions);
    if (edges.length > 0) {
      interventions.push({
        priority: 'low',
        type: 'opportunity',
        message: `${edges.length} validated edge${edges.length > 1 ? 's' : ''} identified`,
        action: 'Increase position size on validated edges'
      });
    }
    
    return interventions.sort((a, b) => {
      const priorityOrder = { high: 0, medium: 1, low: 2 };
      return priorityOrder[a.priority] - priorityOrder[b.priority];
    });
  },
  
  // Generate narrative hero text
  generateHeroState(intelligence) {
    const { summary, interventions } = intelligence;
    
    if (interventions.length === 0) {
      return {
        state: 'Steady state',
        delta: 'No immediate action required',
        sentiment: 'neutral'
      };
    }
    
    const highPriority = interventions.filter(i => i.priority === 'high');
    
    if (highPriority.length > 0) {
      const top = highPriority[0];
      return {
        state: top.message,
        delta: top.action,
        sentiment: 'warning'
      };
    }
    
    return {
      state: `${summary.winRate}% win rate across ${summary.total} predictions`,
      delta: interventions[0].message,
      sentiment: 'positive'
    };
  },
  
  // Generate trading insights
  generateTradingInsights(positions, intelligence) {
    const insights = [];
    
    // Correlation risk
    const rainPositions = positions.filter(p => p.market.includes('Rain'));
    if (rainPositions.length > 2) {
      insights.push({
        type: 'risk',
        severity: 'medium',
        message: `${rainPositions.length} rain positions — correlation risk if weather pattern shifts`,
        recommendation: 'Consider hedging or reducing rain exposure'
      });
    }
    
    // Position sizing
    const totalExposure = positions.reduce((sum, p) => sum + p.amount, 0);
    if (totalExposure > 5) {
      insights.push({
        type: 'sizing',
        severity: 'low',
        message: `Total exposure $${totalExposure.toFixed(2)} — within risk limits`,
        recommendation: 'Maintain current sizing'
      });
    }
    
    // Edge application
    if (intelligence.edges.length > 0) {
      const topEdge = intelligence.edges[0];
      insights.push({
        type: 'opportunity',
        severity: 'positive',
        message: `${topEdge.market}: ${topEdge.confidence}% validation rate`,
        recommendation: 'Increase position size on this market type'
      });
    }
    
    return insights;
  }
};

// Export for use in dashboard
if (typeof module !== 'undefined') module.exports = ContentIntelligence;

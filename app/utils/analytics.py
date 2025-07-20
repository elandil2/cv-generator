from typing import Dict, List
import streamlit as st
import re
from collections import Counter

class CVAnalytics:
    @staticmethod
    def analyze_keyword_match(cv_content: str, job_description: str) -> Dict:
        """Industry-agnostic keyword matching with enhanced technical term detection"""
        
        def extract_important_keywords(text: str) -> Dict[str, int]:
            """Extract keywords with better technical term handling"""
            text_lower = text.lower()
            
            # Remove common stop words
            stop_words = {
                'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
                'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had',
                'do', 'does', 'did', 'will', 'would', 'could', 'should', 'this', 'that',
                'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'who', 'what',
                'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
                'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same',
                'so', 'than', 'too', 'very', 'can', 'just', 'now', 'get', 'may', 'new',
                'work', 'also', 'well', 'way', 'even', 'back', 'good', 'make', 'first',
                'through', 'after', 'without', 'around', 'must', 'need', 'using', 'used',
                'our', 'your', 'their', 'one', 'two', 'three', 'include', 'including'
            }
            
            all_keywords = {}
            
            # 1. Extract important single words (including 2-letter important terms)
            words = re.findall(r'\b[a-z]{2,}\b', text_lower)
            important_single_words = [word for word in words if word not in stop_words]
            
            # 2. Extract specific technical abbreviations and short terms
            tech_patterns = [
                r'\bml\b', r'\bai\b', r'\bapi\b', r'\bsql\b', r'\baws\b', r'\bgcp\b',
                r'\betl\b', r'\bci\b', r'\bcd\b', r'\bui\b', r'\bux\b', r'\bid\b',
                r'\bkpi\b', r'\broi\b', r'\bcrm\b', r'\berp\b', r'\bseo\b', r'\bppc\b',
                r'\bhr\b', r'\bpr\b', r'\bit\b', r'\bqa\b', r'\bba\b', r'\bpm\b'
            ]
            
            for pattern in tech_patterns:
                matches = re.findall(pattern, text_lower)
                for match in matches:
                    all_keywords[match] = all_keywords.get(match, 0) + 2  # Higher weight
            
            # 3. Extract compound terms and phrases
            compound_patterns = [
                r'machine\s+learning', r'deep\s+learning', r'data\s+science', r'data\s+analysis',
                r'artificial\s+intelligence', r'computer\s+vision', r'natural\s+language',
                r'project\s+management', r'product\s+management', r'customer\s+service',
                r'business\s+intelligence', r'software\s+development', r'web\s+development',
                r'quality\s+assurance', r'user\s+experience', r'digital\s+marketing',
                r'financial\s+analysis', r'risk\s+management', r'supply\s+chain',
                r'human\s+resources', r'sales\s+management', r'content\s+creation',
                r'large\s+language\s+models?', r'language\s+models?', r'mlops', r'devops',
                r'data\s+engineering', r'software\s+engineering', r'model\s+deployment',
                r'feature\s+engineering', r'cross\s+functional', r'full\s+stack',
                r'front\s+end', r'back\s+end', r'real\s+time', r'big\s+data'
            ]
            
            for pattern in compound_patterns:
                matches = re.findall(pattern, text_lower)
                for match in matches:
                    clean_match = re.sub(r'\s+', ' ', match.strip())
                    all_keywords[clean_match] = all_keywords.get(clean_match, 0) + 3  # Even higher weight
            
            # 4. Extract acronyms (2-6 uppercase letters)
            acronyms = re.findall(r'\b[A-Z]{2,6}\b', text)
            for acronym in acronyms:
                acronym_lower = acronym.lower()
                all_keywords[acronym_lower] = all_keywords.get(acronym_lower, 0) + 2
            
            # 5. Special handling for LLMs and model terms
            llm_patterns = [
                r'\bllms?\b', r'\bgpt\b', r'\bbert\b', r'\btransformer\b', r'\bneural\s+network',
                r'\bdeep\s+neural', r'\blanguage\s+model', r'\bgenerative\s+ai'
            ]
            
            for pattern in llm_patterns:
                matches = re.findall(pattern, text_lower)
                for match in matches:
                    clean_match = re.sub(r'\s+', ' ', match.strip())
                    all_keywords[clean_match] = all_keywords.get(clean_match, 0) + 3
            
            # 6. Count regular words
            word_counts = Counter(important_single_words)
            for word, count in word_counts.items():
                if word not in all_keywords:  # Don't overwrite higher-weighted terms
                    all_keywords[word] = count
            
            # 7. Special handling for role-specific terms
            role_terms = re.findall(r'\b(engineer|developer|analyst|manager|specialist|coordinator|director|lead|senior|junior|scientist|architect|consultant)\b', text_lower)
            for term in role_terms:
                all_keywords[term] = all_keywords.get(term, 0) + 1.5
            
            # 8. Technology and framework terms
            tech_terms = re.findall(r'\b(python|java|javascript|react|angular|vue|node|docker|kubernetes|terraform|git|jenkins|jira|slack|excel|powerbi|tableau|salesforce|hubspot)\b', text_lower)
            for term in tech_terms:
                all_keywords[term] = all_keywords.get(term, 0) + 2
            
            return all_keywords
        
        # Extract keywords from both texts
        cv_keywords = extract_important_keywords(cv_content)
        job_keywords = extract_important_keywords(job_description)
        
        # Find matches and calculate weighted scores
        matching_keywords = {}
        for keyword, job_freq in job_keywords.items():
            if keyword in cv_keywords:
                # Weight by frequency in job description
                matching_keywords[keyword] = job_freq
        
        # Missing keywords (prioritize by frequency in job description)
        missing_keywords = {k: v for k, v in job_keywords.items() if k not in cv_keywords}
        
        # Calculate match percentage
        if job_keywords:
            total_job_weight = sum(job_keywords.values())
            matched_weight = sum(matching_keywords.values())
            match_percentage = (matched_weight / total_job_weight) * 100
        else:
            match_percentage = 0
        
        # Sort by importance (frequency in job description)
        top_matching = sorted(matching_keywords.items(), key=lambda x: x[1], reverse=True)
        top_missing = sorted(missing_keywords.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "match_percentage": round(match_percentage, 2),
            "matching_keywords": [keyword for keyword, freq in top_matching[:15]],
            "missing_keywords": [keyword for keyword, freq in top_missing[:15]],
            "high_priority_missing": [keyword for keyword, freq in top_missing[:5]],
            "cv_keyword_count": len(cv_keywords),
            "job_keyword_count": len(job_keywords),
            "cv_keywords_detail": cv_keywords,
            "job_keywords_detail": job_keywords
        }
    
    @staticmethod
    def display_analytics_dashboard(cv_content: str, job_description: str):
        """Industry-agnostic analytics dashboard"""
        
        st.markdown("### 📊 CV Analytics Dashboard")
        
        analysis = CVAnalytics.analyze_keyword_match(cv_content, job_description)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            match_pct = analysis['match_percentage']
            if match_pct >= 70:
                st.metric("Keyword Match", f"{match_pct:.1f}%", delta="Excellent", delta_color="normal")
            elif match_pct >= 50:
                st.metric("Keyword Match", f"{match_pct:.1f}%", delta="Good", delta_color="normal")
            else:
                st.metric("Keyword Match", f"{match_pct:.1f}%", delta="Needs Improvement", delta_color="inverse")
        
        with col2:
            st.metric("Matching Keywords", len(analysis['matching_keywords']))
        
        with col3:
            st.metric("High Priority Missing", len(analysis['high_priority_missing']))
        
        # Progress bar for match percentage
        st.progress(min(analysis['match_percentage'] / 100, 1.0))
        
        if analysis['match_percentage'] < 60:
            st.warning("⚠️ Keyword match is low. Consider adding more relevant terms from the missing keywords list.")
        elif analysis['match_percentage'] >= 80:
            st.success("🎉 Excellent keyword match! Your CV is well-optimized for this job.")
        
        # Detailed breakdown
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**✅ Matching Keywords:**")
            if analysis['matching_keywords']:
                for i, keyword in enumerate(analysis['matching_keywords'], 1):
                    st.write(f"{i}. **{keyword}**")
            else:
                st.write("No matching keywords found")
            
            # Show total keywords found
            st.caption(f"Total CV keywords detected: {analysis['cv_keyword_count']}")
        
        with col2:
            st.markdown("**🔥 HIGH PRIORITY Missing:**")
            if analysis['high_priority_missing']:
                for keyword in analysis['high_priority_missing']:
                    st.write(f"• **{keyword}**")
            else:
                st.write("No high priority missing keywords!")
            
            st.markdown("**❌ Other Missing Keywords:**")
            other_missing = analysis['missing_keywords'][5:10]  # Next 5
            if other_missing:
                for keyword in other_missing:
                    st.write(f"• {keyword}")
            else:
                st.write("No other missing keywords")
            
            # Show total job keywords
            st.caption(f"Total job keywords detected: {analysis['job_keyword_count']}")
        
        # Expandable detailed analysis
        with st.expander("🔍 Detailed Keyword Analysis"):
            st.markdown("**All Job Description Keywords (by importance):**")
            job_details = analysis.get('job_keywords_detail', {})
            sorted_job_keywords = sorted(job_details.items(), key=lambda x: x[1], reverse=True)
            
            for keyword, weight in sorted_job_keywords[:20]:
                if keyword in analysis['matching_keywords']:
                    st.write(f"✅ **{keyword}** (weight: {weight})")
                else:
                    st.write(f"❌ {keyword} (weight: {weight})")
        
        # Recommendations
        if analysis['high_priority_missing']:
            st.markdown("### 💡 Recommendations")
            st.info(f"""
            **To improve your CV match:**
            1. Add these high-priority terms: {', '.join(analysis['high_priority_missing'][:3])}
            2. Include specific examples using these keywords
            3. Update your skills section with missing technical terms
            4. Rewrite achievements to include relevant terminology
            """)
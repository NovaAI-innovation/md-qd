import os
import json
import tkinter as tk
from tkinter import filedialog
import re

def split_into_sentences(text):
    """
    Split text into sentences using improved regex pattern that handles:
    - Abbreviations (Dr., Mr., Mrs., Prof., etc.)
    - Numbers and decimals (3.14, version 2.0)
    - Initials (J.R.R., U.S.A.)
    - File extensions and URLs (.com, .py)
    - Multiple sentence endings (!!, ??)
    """
    # Common abbreviations that shouldn't trigger sentence splits
    abbreviations = {
        # Titles
        'Dr', 'Mr', 'Mrs', 'Ms', 'Prof', 'Rev', 'Fr', 'Sr', 'Jr',
        # Academic and professional
        'Ph.D', 'M.D', 'B.A', 'M.A', 'B.S', 'M.S', 'PhD', 'MD',
        # Geographic and organizational  
        'U.S', 'U.K', 'U.S.A', 'U.K', 'EU', 'UN', 'NATO', 'FBI', 'CIA',
        # Time and measurements
        'Jan', 'Feb', 'Mar', 'Apr', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
        'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun',
        'a.m', 'p.m', 'AM', 'PM', 'etc', 'i.e', 'e.g', 'vs', 'vol', 'no',
        # Technical
        'Inc', 'Corp', 'Ltd', 'Co', 'LLC'
    }
    
    # Create a pattern for abbreviations - case insensitive matching
    abbrev_pattern = '|'.join(re.escape(abbr) for abbr in abbreviations)
    
    # Enhanced sentence splitting pattern:
    # - Look for sentence ending punctuation (.!?)
    # - Followed by whitespace and capital letter (or end of string)
    # - But NOT if preceded by known abbreviations
    # - Handle multiple punctuation marks (e.g., "Really?!" or "Wait...")
    
    # First, protect abbreviations by temporarily replacing them
    protected_text = text
    abbrev_replacements = {}
    replacement_counter = 0
    
    # Protect common abbreviations
    for abbrev in abbreviations:
        # Match abbreviation followed by period, case insensitive
        pattern = rf'\b{re.escape(abbrev)}\.'
        matches = list(re.finditer(pattern, protected_text, re.IGNORECASE))
        for match in reversed(matches):  # Process in reverse to maintain positions
            placeholder = f"__ABBREV_{replacement_counter}__"
            abbrev_replacements[placeholder] = match.group(0)
            protected_text = protected_text[:match.start()] + placeholder + protected_text[match.end():]
            replacement_counter += 1
    
    # Protect decimal numbers (e.g., 3.14, 12.5)
    decimal_pattern = r'\b\d+\.\d+\b'
    decimal_matches = list(re.finditer(decimal_pattern, protected_text))
    for match in reversed(decimal_matches):
        placeholder = f"__DECIMAL_{replacement_counter}__"
        abbrev_replacements[placeholder] = match.group(0)
        protected_text = protected_text[:match.start()] + placeholder + protected_text[match.end():]
        replacement_counter += 1
    
    # Protect single-letter initials (e.g., "John T.", "Dr. Aaron T.", "J. R. R.")
    # This handles cases where initials follow names or titles
    initial_pattern = r'\b[A-Z]\.'
    initial_matches = list(re.finditer(initial_pattern, protected_text))
    for match in reversed(initial_matches):
        # Check if this initial follows a word (name) or another initial
        start_pos = match.start()
        if start_pos > 0:
            # Look at the character before to see if it's part of a name
            before_match = protected_text[:start_pos].strip()
            if before_match and (before_match[-1].isalpha() or before_match.endswith('.')):
                placeholder = f"__INITIAL_{replacement_counter}__"
                abbrev_replacements[placeholder] = match.group(0)
                protected_text = protected_text[:match.start()] + placeholder + protected_text[match.end():]
                replacement_counter += 1
    
    # Protect file extensions and URLs (basic protection)
    extension_pattern = r'\b\w+\.[a-zA-Z]{2,4}\b'
    extension_matches = list(re.finditer(extension_pattern, protected_text))
    for match in reversed(extension_matches):
        # Only protect if it looks like a file extension or domain
        matched_text = match.group(0)
        if '.' in matched_text and not matched_text[0].isupper():  # Avoid protecting sentence starts
            placeholder = f"__EXT_{replacement_counter}__"
            abbrev_replacements[placeholder] = matched_text
            protected_text = protected_text[:match.start()] + placeholder + protected_text[match.end():]
            replacement_counter += 1
    
    # Now split sentences on the protected text
    # Split on: sentence ending punctuation + whitespace + capital letter (or end)
    sentence_pattern = r'([.!?]+)\s+(?=[A-Z]|$)'
    sentences = re.split(sentence_pattern, protected_text)
    
    # Reconstruct sentences (the split creates alternating text and punctuation)
    reconstructed_sentences = []
    for i in range(0, len(sentences), 2):
        sentence_text = sentences[i].strip()
        if i + 1 < len(sentences):
            # Add back the punctuation
            sentence_text += sentences[i + 1]
        
        if sentence_text:  # Only add non-empty sentences
            reconstructed_sentences.append(sentence_text)
    
    # Restore protected abbreviations and numbers
    final_sentences = []
    for sentence in reconstructed_sentences:
        for placeholder, original in abbrev_replacements.items():
            sentence = sentence.replace(placeholder, original)
        final_sentences.append(sentence.strip())
    
    # Final cleanup - remove empty sentences
    final_sentences = [s for s in final_sentences if s.strip()]
    
    return final_sentences


def create_semantic_chunks(sentences, max_chunk_size=3, max_chars=500):
    """
    Group sentences into semantic chunks of reasonable size.
    
    Args:
        sentences: List of individual sentences
        max_chunk_size: Maximum number of sentences per chunk
        max_chars: Maximum characters per chunk (soft limit)
    
    Returns:
        List of text chunks (each chunk is a string of combined sentences)
    """
    if not sentences:
        return []
    
    chunks = []
    current_chunk = []
    current_char_count = 0
    
    for sentence in sentences:
        sentence_length = len(sentence)
        
        # Check if adding this sentence would exceed limits
        will_exceed_size = len(current_chunk) >= max_chunk_size
        will_exceed_chars = current_char_count + sentence_length > max_chars
        
        # If adding this sentence would exceed limits and we have content, finalize current chunk
        if (will_exceed_size or will_exceed_chars) and current_chunk:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
            current_char_count = 0
        
        # Add sentence to current chunk
        current_chunk.append(sentence)
        current_char_count += sentence_length
    
    # Add the final chunk if it has content
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks

def smart_chunk_text(text, strategy='sentence', **kwargs):
    """
    Intelligently chunk text using various strategies.
    
    Args:
        text: The text to chunk
        strategy: 'sentence' (individual sentences), 'semantic' (grouped sentences), 'paragraph' (split on double newlines)
        **kwargs: Additional parameters for specific strategies
    
    Returns:
        List of text chunks
    """
    if strategy == 'sentence':
        return split_into_sentences(text)
    
    elif strategy == 'semantic':
        sentences = split_into_sentences(text)
        max_chunk_size = kwargs.get('max_chunk_size', 3)
        max_chars = kwargs.get('max_chars', 500)
        return create_semantic_chunks(sentences, max_chunk_size, max_chars)
    
    elif strategy == 'paragraph':
        # Split on paragraph breaks (double newlines)
        paragraphs = re.split(r'\n\s*\n', text)
        # Clean and filter paragraphs
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        return paragraphs
    
    else:
        raise ValueError(f"Unknown chunking strategy: {strategy}")

def extract_heading_title(line, level):
    """
    Extract the title from a markdown heading line.
    Handles cases where headings and content are on the same line.
    """
    # Remove the heading markers
    heading_content = line.lstrip('#').strip()
    
    # For H3 and below, try to extract just the title part
    if level >= 3:
        # Look for common patterns that indicate the end of a title
        # Title usually ends before the first sentence-ending punctuation
        # or before the first word that starts with lowercase (indicating content)
        
        # Split by sentence endings first
        parts = re.split(r'[.!?]', heading_content, 1)
        if len(parts) > 1:
            # If there's sentence-ending punctuation, take everything before it
            title = parts[0].strip()
            # If title is too long, it might include content - try to find a better break
            if len(title) > 100:
                # Look for natural breaks like "This is" or "This involves" etc.
                break_patterns = [
                    r'^(.*?)\s+(This is|This involves|This technique|This approach|This method|This strategy|This tool|This skill|This example|This pattern)',
                    r'^(.*?)\s+(When we|When you|If you|If we|Let\'s|Here are|Here is|For example|For instance)',
                    r'^(.*?)\s+(The goal|The purpose|The key|The main|The first|The next|The last)',
                    r'^(.*?)\s+(There are|There is|There will|There can|There might|There should)',
                    r'^(.*?)\s+(You can|You will|You might|You should|You need|You have|You are)',
                    r'^(.*?)\s+(We can|We will|We might|We should|We need|We have|We are)'
                ]
                
                for pattern in break_patterns:
                    match = re.search(pattern, title, re.IGNORECASE)
                    if match:
                        title = match.group(1).strip()
                        break
                
                # If still too long, try to find the last capitalized word sequence
                if len(title) > 80:
                    words = title.split()
                    for i in range(len(words) - 1, 0, -1):
                        if words[i][0].isupper() and i > 0:
                            potential_title = ' '.join(words[:i+1])
                            if len(potential_title) <= 80:
                                title = potential_title
                                break
        else:
            title = heading_content
    else:
        # For H1 and H2, just take the whole content as title
        title = heading_content
    
    return title.strip()

def process_heading_line_with_content(line, level):
    """
    Process a heading line that contains content and return both the title and the content.
    This handles cases where headings and content are on the same line.
    """
    # Remove the heading markers
    heading_content = line.lstrip('#').strip()
    
    if level >= 3:
        # For H3 and below, try to separate title from content
        # Look for the first sentence-ending punctuation or natural content breaks
        
        # First, try to find sentence endings
        sentence_match = re.search(r'^([^.!?]+[.!?]?)(.*)', heading_content)
        if sentence_match:
            title = sentence_match.group(1).strip()
            content = sentence_match.group(2).strip()
            
            # If the title is too long, it might include content
            if len(title) > 80:
                # Look for natural content breaks
                break_patterns = [
                    r'^(.*?)\s+(This is|This involves|This technique|This approach|This method|This strategy|This tool|This skill|This example|This pattern)',
                    r'^(.*?)\s+(When we|When you|If you|If we|Let\'s|Here are|Here is|For example|For instance)',
                    r'^(.*?)\s+(The goal|The purpose|The key|The main|The first|The next|The last)',
                    r'^(.*?)\s+(There are|There is|There will|There can|There might|There should)',
                    r'^(.*?)\s+(You can|You will|You might|You should|You need|You have|You are)',
                    r'^(.*?)\s+(We can|We will|We might|We should|We need|We have|We are)'
                ]
                
                for pattern in break_patterns:
                    match = re.search(pattern, heading_content, re.IGNORECASE)
                    if match:
                        title = match.group(1).strip()
                        content = heading_content[len(title):].strip()
                        break
                
                # If still too long, try to find the last capitalized word sequence
                if len(title) > 60:
                    words = title.split()
                    for i in range(len(words) - 1, 0, -1):
                        if words[i][0].isupper() and i > 0:
                            potential_title = ' '.join(words[:i+1])
                            if len(potential_title) <= 60:
                                title = potential_title
                                content = heading_content[len(title):].strip()
                                break
        else:
            # No sentence ending found, try to find content breaks
            title = heading_content
            content = ""
            
            # Look for natural content breaks
            break_patterns = [
                r'^(.*?)\s+(This is|This involves|This technique|This approach|This method|This strategy|This tool|This skill|This example|This pattern)',
                r'^(.*?)\s+(When we|When you|If you|If we|Let\'s|Here are|Here is|For example|For instance)',
                r'^(.*?)\s+(The goal|The purpose|The key|The main|The first|The next|The last)',
                r'^(.*?)\s+(There are|There is|There will|There can|There might|There should)',
                r'^(.*?)\s+(You can|You will|You might|You should|You need|You have|You are)',
                r'^(.*?)\s+(We can|We will|We might|We should|We need|We have|We are)'
            ]
            
            for pattern in break_patterns:
                match = re.search(pattern, heading_content, re.IGNORECASE)
                if match:
                    title = match.group(1).strip()
                    content = heading_content[len(title):].strip()
                    break
        
        # Clean up the title - remove any duplicate words at the beginning
        # This handles cases like "Mindfulness Mindfulness is the practice..."
        title_words = title.split()
        if len(title_words) > 1 and title_words[0].lower() == title_words[1].lower():
            # Remove the duplicate first word
            title = ' '.join(title_words[1:])
            # Add the duplicate word back to content if it was part of the original
            if content and not content.startswith(title_words[0]):
                content = title_words[0] + ' ' + content
        
        # Additional cleanup: if title ends with a word that's repeated at the start of content
        if content and title and title.split()[-1].lower() == content.split()[0].lower():
            # Remove the last word from title if it's the same as the first word in content
            title_words = title.split()
            if len(title_words) > 1:
                title = ' '.join(title_words[:-1])
                # Don't modify content here as it might break the flow
                
    else:
        # For H1 and H2, just take the whole content as title
        title = heading_content
        content = ""
    
    return title.strip(), content.strip()

def chunk_markdown_file(file_path, filename):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    sentences_data = []
    
    # Initialize heading contexts - only track H1, H2, and H3
    current_h1 = None
    current_h2 = None
    current_h3 = None

    for i, line in enumerate(lines):
        line = line.strip()
        if not line:  # Skip empty lines
            continue

        # Check if the line starts with a hash, indicating a markdown heading
        if line.startswith('#'):
            match = re.match(r'^(#+)\s*(.*)', line)
            if match:
                level = len(match.group(1))
                title, content = process_heading_line_with_content(line, level)

                # Only track H1, H2, and H3 levels
                if level == 1:
                    current_h1 = title
                    current_h2 = None
                    current_h3 = None
                elif level == 2:
                    current_h2 = title
                    current_h3 = None
                elif level == 3:
                    current_h3 = title
                # Ignore H4, H5, and H6 levels
                
                # If there's content on the same line as the heading, process it
                if content:
                    raw_sentences = split_into_sentences(content)
                    for sentence in raw_sentences:
                        sentence = sentence.strip()
                        if sentence:  # Ensure sentence is not empty
                            sentences_data.append({
                                'text': sentence,
                                'source_file': filename,
                                'chapter_name': current_h1,
                                'section_name': current_h2,
                                'subsection_name': current_h3
                            })
        else:
            # Process non-heading text into sentences
            raw_sentences = split_into_sentences(line)
            for sentence in raw_sentences:
                sentence = sentence.strip()
                if sentence:  # Ensure sentence is not empty
                    sentences_data.append({
                        'text': sentence,
                        'source_file': filename,
                        'chapter_name': current_h1,
                        'section_name': current_h2,
                        'subsection_name': current_h3
                    })
    
    return sentences_data

def main():
    root = tk.Tk()
    root.withdraw()

    input_directory = filedialog.askdirectory(title="Select Input Directory")

    if not input_directory:
        print("No directory selected. Exiting.")
        return

    for root, _, files in os.walk(input_directory):
        for filename in files:
            if filename.endswith(".md"):
                md_file_path = os.path.join(root, filename)
                json_output = chunk_markdown_file(md_file_path, filename)
                
                json_file_path = os.path.join(root, os.path.splitext(filename)[0] + ".json")
                
                with open(json_file_path, 'w', encoding='utf-8') as f:
                    json.dump(json_output, f, indent=4, ensure_ascii=False)
                
                print(f"Processed {md_file_path} -> {json_file_path}")

if __name__ == "__main__":
    main()
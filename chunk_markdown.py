import os
import json
import tkinter as tk
from tkinter import filedialog
import re

def split_into_sentences(text):
    """Split text into sentences using regex pattern."""
    # Split on sentence endings: .!? followed by whitespace or end of string
    sentences = re.split(r'[.!?]+\s+', text)
    # Clean up sentences and filter out empty ones
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences

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
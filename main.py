import ai21
import tkinter as tk
from tkinter import simpledialog

ai21.api_key = '2e9ma65RIrdwSIWlV8ODunDPdMA0gUF0'

def configure_bold_tag(text_widget):
    text_widget.tag_configure("bold", font=("Helvetica", 12, "bold"))

stored_text = ""  # Variable to store the entered text

def store_input_text():
    global stored_text
    stored_text = input_text.get("1.0", tk.END).strip()

def show_improved_text():
    result = input_text.get("1.0", tk.END).strip()

    if not result:
        print("请输入文本")
        return

    # Check if there's stored text from previous input
    if stored_text:
        # Use the stored text instead of making a new API request
        result = stored_text

    response = ai21.Improvements.execute(text=result, types=["fluency"])
    improvements = response["improvements"]
    print(response)

    output_text.delete("1.0", tk.END)  # Clear previous content

    if improvements:
        # If there are improvements, display the originalText and suggestions
        for improvement in improvements:
            original_text = improvement.originalText  # Access the originalText attribute directly
            output_text.insert(tk.END, "Original Text: ")
            output_text.insert(tk.END, original_text, "bold")
            output_text.insert(tk.END, "\n\n")

            suggestions = improvement["suggestions"]
            for i, suggestion in enumerate(suggestions, start=1):
                suggestion_text = suggestion.split(" ", 1)  # Split the suggestion into two parts: first word and the rest
                first_word = suggestion_text[0]
                rest_of_suggestion = suggestion_text[1] if len(suggestion_text) > 1 else ""

                formatted_suggestion = f"\nSuggestion {i}: {first_word}{rest_of_suggestion}"

                # Apply the bold tag to the first 12 characters of the current suggestion
                start_index = output_text.index(tk.END)
                end_index = f"{start_index}+12c"
                output_text.insert(tk.END, formatted_suggestion)
                output_text.tag_add("bold", start_index, end_index)

    else:
        # If there are no improvements, display a specific message
        output_text.insert(tk.END, "没有可以修改的地方，建议使用别的功能")

    # Clear the input text box after displaying improved text
    input_text.delete("1.0", tk.END)

def generate_response():
    result = input_text.get("1.0", tk.END).strip()

    if result:
        response = ai21.Paraphrase.execute(text=result, startIndex=0)
        output_text.delete("1.0", tk.END)

        for i, suggestion in enumerate(response['suggestions'], start=1):
            output_text.insert(tk.END, f"{i}. {suggestion['text']}\n\n")

    else:
        print("请输入文本")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("AI Response Generator")

    input_frame = tk.Frame(root)
    input_frame.pack(pady=10)

    input_label = tk.Label(input_frame, text="请输入文本内容：")
    input_label.pack(side=tk.LEFT)

    input_text = tk.Text(input_frame, height=5, width=50)
    input_text.pack(side=tk.LEFT)

    generate_button = tk.Button(root, text="生成响应", command=generate_response)
    generate_button.pack(pady=10)

    show_improved_button = tk.Button(root, text="显示改进后的文本", command=show_improved_text)
    show_improved_button.pack(pady=10)

    output_text = tk.Text(root, height=10, width=50)
    output_text.pack()
    configure_bold_tag(output_text)

    root.mainloop()

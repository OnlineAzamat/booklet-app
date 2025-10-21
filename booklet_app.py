import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pypdf import PdfReader, PdfWriter
import math
import os

# -----------------------------------------------
# I. CORE LOGIC FUNCTIONS
# -----------------------------------------------
def calculate_booklet_pages(total_pages):
  """The book calculates the page order for printing."""
  if total_pages <= 0: return [], []
  pages_per_sheet = 4
  num_sheets = math.ceil(total_pages / pages_per_sheet)
  padded_total_pages = num_sheets * pages_per_sheet
  pages = list(range(1, total_pages + 1))
  pages.extend([0] * (padded_total_pages - total_pages))
  
  old_tomon_sahifalari = []
  orqa_tomon_sahifalari = []
  start = 0
  end = padded_total_pages - 1
  
  while start < end:
    old_tomon_sahifalari.append(pages[end])
    old_tomon_sahifalari.append(pages[start])
    orqa_tomon_sahifalari.append(pages[start + 1])
    orqa_tomon_sahifalari.append(pages[end - 1])
    start += 2
    end -= 2
      
  return old_tomon_sahifalari, orqa_tomon_sahifalari

def generate_page_list_string(total_pages):
  """Returns the list of front and back pages separately."""
  if not isinstance(total_pages, int) or total_pages <= 0:
    return "Qáte: Betler sanı on pútin san boliwi kerek.", "Qátelik"

  old_pages_with_zeros, back_pages_with_zeros = calculate_booklet_pages(total_pages)
  
  # Ignore blank pages (0)
  old_list = [str(p) for p in old_pages_with_zeros if p != 0]
  back_list = [str(p) for p in back_pages_with_zeros if p != 0]

  return old_list, back_list

# -----------------------------------------------
# II. GUI
# -----------------------------------------------
class BookletApp:
  def __init__(self, master):
    self.master = master
    master.title("Kıtap Pechat (Yakubbaev Azamat)")
    # Window: 650x450
    master.geometry("650x450")
    
    self.input_file_path = tk.StringVar()
    self.start_page_var = tk.StringVar(value="1")
    self.end_page_var = tk.StringVar()
    self.total_pdf_pages = 0
    
    # Variables for dividing sheets
    self.wrap_sheets_var = tk.StringVar(value="10")
    self.wrap_enabled = tk.BooleanVar(value=False)
    
    self.notebook = ttk.Notebook(master)
    self.notebook.pack(pady=10, padx=10, expand=True, fill='both')

    self._create_widgets_pdf_processor()
    self._create_widgets_calculator()

  def _create_widgets_pdf_processor(self):
    # Section 1 - Preparation of a PDF Document
    frame_pdf = ttk.Frame(self.notebook, padding="10")
    self.notebook.add(frame_pdf, text='1. PDF Dokument Tayarlaw')
    
    # Select File
    frame_file = ttk.Frame(frame_pdf)
    frame_file.pack(fill='x', pady=5)
    ttk.Label(frame_file, text="PDF Fayl:").pack(side='left', padx=(0, 5))
    self.entry_file = ttk.Entry(frame_file, textvariable=self.input_file_path, width=50, state='readonly')
    self.entry_file.pack(side='left', fill='x', expand=True, padx=(0, 5))
    ttk.Button(frame_file, text="Tańlaw...", command=self.select_pdf_file).pack(side='left')

    # Paging
    frame_pages = ttk.Frame(frame_pdf)
    frame_pages.pack(fill='x', pady=5)
    ttk.Label(frame_pages, text="Baslanǵısh beti:").pack(side='left', padx=(0, 5))
    self.entry_start = ttk.Entry(frame_pages, textvariable=self.start_page_var, width=10)
    self.entry_start.pack(side='left', padx=(0, 20))
    ttk.Label(frame_pages, text="Aqırǵı beti:").pack(side='left', padx=(0, 5))
    self.entry_end = ttk.Entry(frame_pages, textvariable=self.end_page_var, width=10)
    self.entry_end.pack(side='left')

    # Print button
    ttk.Button(frame_pdf, text="Kitap Formatında Dokumentti Tayarlaw (2 x PDF)", 
                command=self.process_pdf, style='TButton').pack(pady=20)
    
    # Status field (PDF section only)
    self.status_text_pdf = tk.Text(frame_pdf, height=8, state='disabled', wrap='word')
    self.status_text_pdf.pack(fill='both', expand=True, pady=5)
        
  def _create_widgets_calculator(self):
    # Section 2 - Calculating Page Order
    frame_calc = ttk.Frame(self.notebook, padding="10")
    self.notebook.add(frame_calc, text='2. Betler Tártibin Esaplaw (Printer ushın)')
    
    # Page range (Reusable)
    frame_pages_calc = ttk.Frame(frame_calc)
    frame_pages_calc.pack(fill='x', pady=5)
    ttk.Label(frame_pages_calc, text="Baslanǵısh beti:").pack(side='left', padx=(0, 5))
    ttk.Entry(frame_pages_calc, textvariable=self.start_page_var, width=10).pack(side='left', padx=(0, 20))
    ttk.Label(frame_pages_calc, text="Aqırǵı beti (Jámi Betler Sanın Kiritiń):").pack(side='left', padx=(0, 5))
    ttk.Entry(frame_pages_calc, textvariable=self.end_page_var, width=10).pack(side='left')
    
    # Splitting option
    frame_wrap = ttk.Frame(frame_calc)
    frame_wrap.pack(fill='x', pady=5)
    
    ttk.Checkbutton(frame_wrap, text="Listlerge Bóliw (Wrapper)", variable=self.wrap_enabled).pack(side='left')
    ttk.Label(frame_wrap, text=" Hár bir pechatda betler sanı:").pack(side='left', padx=(10, 5))
    ttk.Entry(frame_wrap, textvariable=self.wrap_sheets_var, width=5).pack(side='left')
    
    # Calculation button
    ttk.Button(frame_calc, text="Tártip Nomerlerdi Esaplaw", 
                command=self.calculate_only_page_numbers).pack(pady=10)
                
    # Status field (Calculation section only)
    self.status_text_calc = tk.Text(frame_calc, height=10, state='disabled', wrap='word')
    self.status_text_calc.pack(fill='both', expand=True, pady=5)

  def log_status(self, message, is_error=False, tab_index=0):
    """Write a message in the status field (specifies which tab it is)."""
    text_widget = self.status_text_pdf if tab_index == 0 else self.status_text_calc
    text_widget.config(state='normal')
    text_widget.delete(1.0, tk.END)
    if is_error:
      text_widget.insert(tk.END, f"QÁTELIK: {message}", 'error')
      text_widget.tag_config('error', foreground='red')
    else:
      text_widget.insert(tk.END, message)
    text_widget.config(state='disabled')

  def select_pdf_file(self):
    f_path = filedialog.askopenfilename(
      defaultextension=".pdf",
      filetypes=[("PDF files", "*.pdf")]
    )
    if f_path:
      self.input_file_path.set(f_path)
      self.log_status(f"Fayl tańlandı: {f_path}", tab_index=0)
      
      try:
        reader = PdfReader(f_path)
        self.total_pdf_pages = len(reader.pages)
        self.end_page_var.set(str(self.total_pdf_pages)) 
        self.log_status(f"Fayl tańlandı. Jámi betler: {self.total_pdf_pages}. Aqırǵı bet  avtomatik toltırıldı.", tab_index=0)
      except Exception as e:
        self.log_status(f"PDF hújjet betlerin oqıwda qátelik: {e}", is_error=True, tab_index=0)
        self.total_pdf_pages = 0
        self.end_page_var.set("")
              
  def validate_and_get_pages(self, check_file=True):
    """Validates the number of pages entered."""
    # Determine which tab's status box to write to
    current_tab_index = self.notebook.index(self.notebook.select())

    # We'll add a check for file_path only
    file_path = self.input_file_path.get()
    if check_file and (not file_path or not os.path.exists(file_path)):
      self.log_status("Iltimas, PDF fayldı tańlań.", is_error=True, tab_index=current_tab_index)
      return None, None
        
    try:
      start = int(self.start_page_var.get())
      end = int(self.end_page_var.get())
    except ValueError:
      self.log_status("Baslanǵısh hám Aqırǵı betleri pútin san bolıwı kerek.", is_error=True, tab_index=self.notebook.index(self.notebook.select()))
      return None, None
        
    if start < 1 or end < 1 or start > end:
      self.log_status("Betlew diapazoni naduris. (Oń san hám Baslanǵısh <= Aqırǵı boliwi kerek).", is_error=True, tab_index=self.notebook.index(self.notebook.select()))
      return None, None
        
    if check_file and end > self.total_pdf_pages:
      self.log_status(f"Aqırǵı beti PDF daǵı jámi betler sanınan ({self.total_pdf_pages}) úlken.", is_error=True, tab_index=0)
      return None, None
    
    num_pages_to_process = end - start + 1

    if num_pages_to_process % 4 != 0:
      # 4 ke eseli bolǵan jańa betler sanın esaplaymız
      pages_per_sheet = 4
      num_sheets = math.ceil(num_pages_to_process / pages_per_sheet)
      padded_total_pages = int(num_sheets * pages_per_sheet)

      # Padding muǵdarın esaplaymız
      padding_needed = padded_total_pages - num_pages_to_process

      warning_msg = (
        f"Dıqqat: Pechat qılıw ushın betler sanı ({num_pages_to_process}) 4 ke bólinbeydi.\n"
        f"Kitap formatında shıǵarıw ushın {padding_needed} bos bet qosıladı.\n"
        f"Jámi betler sanı {padded_total_pages} ge aylanadı."
      )

      if current_tab_index == 0:
        # PDF tayarlawda: Tek eskertiw beremiz hám processti dawam etemiz.
        self.log_status(warning_msg, tab_index=current_tab_index)

      elif current_tab_index == 1:
        # Esaplawda: Eskertiw beremiz hám tuwrılanǵan sandı usınıs etemiz.
        error_msg = (
          f"Betler sanı ({num_pages_to_process}) 4 ke bólinbeydi. Kitapsha ushın {padding_needed} bos bet kerek.\n"
          f"Iltimas, Aqırǵı bet sanın {end + padding_needed} ge ózgertiń (yáki 4 ke eseli san kiritiń)."
        )
        self.log_status(error_msg, is_error=True, tab_index=current_tab_index)

        # Esaplaw processin toqtatamız, paydalanıwshı tuwrılasın
        return None, None
        
    return start, end

  def process_pdf(self):
    start_page, end_page = self.validate_and_get_pages(check_file=True)
    if start_page is None: return

    input_pdf_path = self.input_file_path.get()
    self.log_status("Process baslandı...", tab_index=0)
    
    try:
      reader = PdfReader(input_pdf_path)
      num_pages_to_process = end_page - start_page + 1
      old_pages, back_pages = calculate_booklet_pages(num_pages_to_process)
      
      output_dir = filedialog.askdirectory(title="Qoyıw papkasın tańlań")
      if not output_dir:
        self.log_status("Qoyıw papkası tańlanbadı. Nátiyjede process biykar etildi.", tab_index=0)
        return

      base_name = os.path.splitext(os.path.basename(input_pdf_path))[0]
      old_writer = PdfWriter()
      back_writer = PdfWriter()

      # The logic of extracting pages and adding them to a new PDF
      for page_num in old_pages:
        if page_num == 0:
          old_writer.add_blank_page(width=reader.pages[0].mediabox.width, height=reader.pages[0].mediabox.height)
        else:
          original_index = (start_page - 1) + (page_num - 1)
          old_writer.add_page(reader.pages[original_index])

      for page_num in back_pages:
        if page_num == 0:
          back_writer.add_blank_page(width=reader.pages[0].mediabox.width, height=reader.pages[0].mediabox.height)
        else:
          original_index = (start_page - 1) + (page_num - 1)
          back_writer.add_page(reader.pages[original_index])

      # Write files
      old_output_path = os.path.join(output_dir, f"{base_name}_ALDI_TÁREP.pdf")
      back_output_path = os.path.join(output_dir, f"{base_name}_ARQA_TÁREP.pdf")
      
      with open(old_output_path, "wb") as f: old_writer.write(f)
      with open(back_output_path, "wb") as f: back_writer.write(f)
          
      self.log_status(f"✅ Process tabıslı juwmaqlandı!\n1. Aldi tárepi: {old_output_path}\n2. Arqa tárepi: {back_output_path}", tab_index=0)
      messagebox.showinfo("Tabıslı", "Kitap formatındaǵı PDF fayllar tayarlandı!")

    except Exception as e:
      error_msg = f"Kútilmegen qátelik júz berdi: {e}"
      self.log_status(error_msg, is_error=True, tab_index=0)
      messagebox.showerror("Qátelik", error_msg)

  def calculate_only_page_numbers(self):
    """A function for calculating only the order of digits."""
    
    start_page, end_page = self.validate_and_get_pages(check_file=False)
    if start_page is None: return
    
    total_pages = end_page - start_page + 1
    
    # Separate front and back lists
    old_list, back_list = generate_page_list_string(total_pages)
    
    if old_list == "Qátelik":
      self.log_status(back_list, is_error=True, tab_index=1)
      return

    # Splitting logic
    wrap_sheets = 0
    try:
      if self.wrap_enabled.get():
        wrap_sheets = int(self.wrap_sheets_var.get())
        if wrap_sheets <= 0:
          self.log_status("Betler sanı oń pútin san boliwi kerek.", is_error=True, tab_index=1)
          return
    except ValueError:
      self.log_status("Betler sanı naduris kiritilgen.", is_error=True, tab_index=1)
      return
    
    old_output_str = self._format_page_list(old_list, wrap_sheets, start_page)
    back_output_str = self._format_page_list(back_list, wrap_sheets, start_page)
    
    formatted_message = (
      "--- ALDI TÁREPI USHIN NOMERLER ---\n"
      f"{old_output_str}\n\n"
      "--- ARQA TÁREPI USHIN NOMERLER ---\n"
      f"{back_output_str}\n\n"
      "Dıqqat: Bul nomerlerdi printer dialogında qolda kirgiziwińiz kerek."
    )
    self.log_status(formatted_message, tab_index=1)

  def _format_page_list(self, page_list, wrap_sheets, start_page):
    """Formats the page list and, if necessary, divides it into sections."""
    
    # Customize to original pages (unless Start=1)
    # Our generate_page_list_string always starts with 1.
    # If the user asked for "from 10 to 50," it will be from 1 to 41.
    # We need to ensure that these 41 digits return starting from 10.
    page_offset = start_page - 1 
    adjusted_list = [str(int(p) + page_offset) for p in page_list]
    
    if wrap_sheets > 0:
      # 1 has 2 front pages (or 2 back pages).
      # Therefore wrap_sheets * We'll be in 2 steps.
      pages_per_wrap = wrap_sheets * 2 
      
      output_parts = []
      for i in range(0, len(adjusted_list), pages_per_wrap):
        chunk = adjusted_list[i:i + pages_per_wrap]
        output_parts.append(",".join(chunk))
      
      return "\n\n" + "\n".join(output_parts)
    else:
      return ",".join(adjusted_list)

if __name__ == "__main__":
  root = tk.Tk()
  app = BookletApp(root)
  root.mainloop()
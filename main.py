import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver # tested with Version 4.35.0
from seleniumbase import SB # tested with Version 4.41.0
from PyPDF2 import  PdfReader, PdfMerger # tested with Version 3.0.1

def wileygetter(url:str, directory:str|os.PathLike):
	"""Collect all pdfs from the chapters given in the url."""
	# Start the driver in uc mode, so that it won't get blocked by antibot detection. This can yield different errors that don't impact the outcome, so try and see if it works. 
	with SB(uc=True, xvfb=True) as sb:
		try:
			sb.uc_open_with_reconnect(url, reconnect_time=3)
		except PermissionError as e:
			print("Pass:", e)
			pass

		try:
			sb.uc_gui_click_captcha()
		except PermissionError as e:
			print("Pass:", e)
			pass
		response = sb.get_page_source()

	# Parse the returned HTML using BeautifulSoup
	parsed = BeautifulSoup(response, "lxml")

	# Find the title in the parsed HTML
	title = parsed.find("meta", property="og:title")
	title = title["content"]

	# Remove a possible space at the beginning of the title
	if title[0] == " ":
		title = title[1:]

	# Get all the links and transform them into downloadadble ones. I suppose that these links could vary for different documents.
	links = parsed.find_all("a", title="EPDF")
	links = [s["href"] for s in links]
	links = [s.replace("epdf", "pdfdirect") for s in links]

	# Create a temporery folder for each chapter pdf
	os.mkdir(f"{directory}{title}")

	# Download every PDF
	for pdfurl in links:
		# Some options for downloading the pdf
		options = webdriver.ChromeOptions()
		options.add_experimental_option('prefs', {
		"download.default_directory": f"{directory}{title}", #Change default directory for downloads
		"download.prompt_for_download": False, #To auto download the file
		"download.directory_upgrade": True,
		"plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
		})

		# Start the normal driver here, it seems to do just fine and should be a little bit quicker
		driver = webdriver.Chrome(options=options)
		num_of_pdf_before_download = len([f for f in os.listdir(f"{directory}{title}") if f.endswith(".pdf")])
		driver.get(pdfurl)

		# Test if a new pdf file appeared and close driver only when it is done.
		while len([f for f in os.listdir(f"{directory}{title}") if f.endswith(".pdf")]) == num_of_pdf_before_download:
			time.sleep(0.5)
		driver.quit()

	# Get the name of all downloaded files
	search_dir = f"{directory}{title}"
	os.chdir(search_dir) # Change into the directory
	# Filter for real files
	files = filter(os.path.isfile, os.listdir(search_dir))
	# Now reduce list to contain only names of pdf files
	files = [f for f in files if f.endswith(".pdf")]
	# Construct a full path out of these files
	files = [os.path.join(search_dir, f) for f in files] 
	# Change for the latest date of change. This assumes that the files downloaded chronologically
	files.sort(key=lambda x: os.path.getmtime(x))

	# Do some processing if no EOF marker is present in the pdf. This will otherwise lead to merge errors
	EOF_MARKER = b'%%EOF'
	for pdffile in files:
		with open(pdffile, 'rb') as f:
			contents = f.read()

		# Check if EOF is somewhere else in the file
		if EOF_MARKER in contents:
			# We can remove the early %%EOF and put it at the end of the file
			contents = contents.replace(EOF_MARKER, b'')
			contents = contents + EOF_MARKER
		else:
			# Some files really don't have an EOF marker
			# In this case it helped to manually review the end of the file
			contents = contents[:-6] + EOF_MARKER
		with open(pdffile, "wb") as f:
			f.write(contents)

		# Now merge all the files together to one big pdf
		merger = PdfMerger()
		merger.append(PdfReader(pdffile))
		#os.remove(pdffile)

	# Go one directory upwards
	merger.write(os.path.normpath(os.getcwd() + os.sep) + ".pdf")
	print(f"Finished Processing : {url}")
	return

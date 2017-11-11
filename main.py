from Tkinter import *
import tkFileDialog
from PIL import Image, ImageTk

from redeye import fix_red_eyes
from selective_blur import blur

class GUI:
	def __init__(self, master):
		frame = Frame(master)
		frame.pack()

		self.file_address = None
		self.img = None
		self.out = None
		self.input_label = None
		self.output_label = None
		self.imheight = 512
		self.imwidth = 512
		
		# selection for segmentation
		self.point1 = None
		self.point2 = None
		self.rect = None

		# input
		self.input_frame = Canvas(frame, height=self.imheight, width=self.imwidth, borderwidth=1, relief=RIDGE)
		self.input_frame.pack(side=LEFT)
		self.input_frame.bind("<Button-1>", self.callback)
		self.input_frame.pack_propagate(False)

		# centre frame for options
		self.center_frame = Frame(frame, height=self.imheight, width=max(128, self.imwidth/4))
		self.center_frame.pack(side=LEFT)

		self.process_indicator = IntVar()
		self.process_indicator.set(1)
		Radiobutton(self.center_frame, text="Red Eye Reduction", variable=self.process_indicator, value=1).pack(anchor=CENTER)
		Radiobutton(self.center_frame, text="Selective Blur", variable=self.process_indicator, value=2).pack(anchor=CENTER)

		self.bUpload = Button(self.center_frame, text="Upload Image", command=self.upload)
		self.bUpload.pack(side=LEFT)
		
		self.bProcess = Button(self.center_frame, text="Process Image", command=self.process)
		self.bProcess.pack(side=LEFT)

		# output
		self.output_frame = Canvas(frame, height=self.imheight, width=self.imwidth, borderwidth=1, relief=RIDGE)
		self.output_frame.pack(side=LEFT)
		self.output_frame.pack_propagate(False)

	def upload(self):
		self.file_address = tkFileDialog.askopenfilename(initialdir = ".",title = "Select Image to be Processed", filetypes=(("JPG Files","*.jpg"), ("PNG Files","*.png")))
		self.img = ImageTk.PhotoImage(Image.open(self.file_address).resize((self.imheight, self.imwidth), Image.ANTIALIAS))
		
		if self.rect is not None:
			self.input_frame.delete(self.point1)
			self.input_frame.delete(self.point2)
			self.input_frame.delete(self.rect)

			self.point1 = None
			self.point2 = None
			self.rect = None

		if self.input_label is None:
			self.input_label = self.input_frame.create_image(self.imwidth/2 + 1, self.imheight/2 + 1, image=self.img)
		else:
			self.input_frame.itemconfig(self.input_label, image=self.img)
			
	def process(self):
		if self.img is not None:
			print "Found image"
			if self.process_indicator.get() == 1:
				print "Removing red eyes"
				self.out = ImageTk.PhotoImage(fix_red_eyes(Image.open(self.file_address).resize((self.imheight, self.imwidth), Image.ANTIALIAS)))

			elif self.process_indicator.get() == 2:
				print "Selective Blurring"
				if self.rect is None:
					print "Please select two points for the rectangle"
				else:
					self.out = ImageTk.PhotoImage(blur(Image.open(self.file_address).resize((self.imheight, self.imheight), Image.ANTIALIAS),
						self.input_frame.coords(self.point1)[0]+3, self.input_frame.coords(self.point1)[1]+3, self.input_frame.coords(self.point2)[0]+3, self.input_frame.coords(self.point2)[1]+3))

			if self.output_label is None:
				self.output_label = Label(self.output_frame, image=self.out)
			else:
				self.output_label.configure(image=self.out)

			self.output_label.image = self.out
			self.output_label.pack()

		else:
			print "Please load image!"

	# take input from the input frame
	def callback(self, event):
		x, y = self.input_frame.canvasx(event.x), self.input_frame.canvasy(event.y)
		
		if self.rect is not None:
			self.input_frame.delete(self.point1)
			self.input_frame.delete(self.point2)
			self.input_frame.delete(self.rect)

			self.point1 = self.input_frame.create_oval(x - 3, y - 3, x + 3, y + 3, fill="Black")
			self.point2 = None
			self.rect = None
		
		elif self.point1 is None:
			self.point1 = self.input_frame.create_oval(x-3, y-3, x+3, y+3, fill="Black")

		elif self.point2 is None:
			self.point2 = self.input_frame.create_oval(x-3, y-3, x+3, y+3, fill="Black")
			self.rect = self.input_frame.create_rectangle(self.input_frame.coords(self.point1)[0]+3, self.input_frame.coords(self.point1)[1]+3, self.input_frame.coords(self.point2)[0]+3, self.input_frame.coords(self.point2)[1]+3)

def main():
	root = Tk()
	root.title("Image Processing 101")
	gui = GUI(root)
	root.mainloop()

if __name__ == '__main__':
	main()
#coding=utf-8

import traceback

if __name__=='__main__':
	import comtypes.client,time
	import  os
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "science.settings")
	from core.models import ConvertPDFTask

	def Doc2Pdf(input, output):
		word = comtypes.client.CreateObject('Word.Application')
		try:
			word.Visible=False
			doc = word.Documents.Open(input)
			doc.SaveAs(output, FileFormat=17)
			doc.Close()
		except:
			print traceback.format_exc()
		finally:
			word.Quit()

	while True:
		tasks=ConvertPDFTask.objects.all()
		pks=[t.pk for t in tasks]
		for t in tasks:
			t.Run(Doc2Pdf)
		time.sleep(10)





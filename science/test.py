from settings import WordTemplates

if __name__=='__main__':

	print WordTemplates.TWord_ProjectApply.substitute(
		project_name='project_name',
		project_type__name='project_type__name',
		project_no='project_type__name',
		applicant__name='applicant__name',
		applicant_opinion='applicant_opinion'
	)

from ethiclean.report import ReportGenerator

reporter = ReportGenerator()
reporter.generate_report_from_csv('test_data.csv', 'gender')

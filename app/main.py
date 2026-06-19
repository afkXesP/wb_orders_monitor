from app.services.report_service import ReportService

def main():
    service = ReportService()
    service.run_daily_pipeline()

if __name__ == "__main__":
    main()
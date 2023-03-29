from server.enquiry_submitter import EnquirySubmitter


def main():
    enquiry_submitter = EnquirySubmitter(
        gs_private_key="<your_gs_private_key>",
        gs_client_email="<your_gs_client_email>",
        gs_token_uri="<your_gs_token_uri>",
        spreadsheet_key="<your_spreadsheet_key>",
        worksheet_title="<your_worksheet_title>",
        timestamp_format="<your_timestamp_format>",
    )

    status = enquiry_submitter.submit({
        "timestamp": 1679798817607,
        "first_name": "Clyde",
        "last_name": "Cronshaw",
        "email": "ccronshaw3@theguardian.com",
        "company": "Topicblab",
        "message": "Nulla tellus. In sagittis dui vel nisl. Duis ac nibh."
    })

    print(status)
    print(enquiry_submitter.message)
    print(enquiry_submitter.detailed_error)
    print(enquiry_submitter.status_code)


if __name__ == "__main__":
    main()

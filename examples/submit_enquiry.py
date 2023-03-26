from server.enquiry_submitter import EnquirySubmitter


def main():
    enquiry_submitter = EnquirySubmitter()

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

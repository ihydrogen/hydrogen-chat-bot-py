import bot_header

def main(cmd):
    print("main")
    print(":\n %d LP requests\n %d messages received\n %d messages sent."
          "\n %s API requests done"
          "\n %s API requests failed"
          "" % (
              bot_header.LP_REQUESTS_DONE,
              bot_header.LP_MESSAGES_RECEIVED,
              bot_header.LP_MESSAGES_SENT,
              bot_header.API_REQUESTS,
              bot_header.FAILED_API_REQUESTS
          ))
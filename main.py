from app import init_app, init_db, init_telegram
import logging


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def main():

    init_db()
    updater = init_telegram()
    app = init_app()

    updater.start_polling()
    app.run(host="0.0.0.0", port=8080, debug=False)


if __name__ == '__main__':
    main()

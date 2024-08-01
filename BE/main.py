from app.routes import app

if __name__ == '__main__':
  # run app in debug mode on port 8080
  app.run(debug=True, port=8080, host='0.0.0.0')
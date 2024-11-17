Link Content Viewer
===================

A simple web service that fetches and displays the content of a URL provided via the endpoint `http://localhost:8000/`.


🚀 Features
-----------

*   Scalable Selenium Grid with Docker Compose.
*   Pre-configured services (Hub, Nodes).
*   Fetch content from any publicly accessible URL
*   Easy to set up with Docker

🛠 Setup and Usage
------------------

1.  Clone the repository:
```bash
git clone https://github.com/vladkanatov/grid-test.git
cd grid-test
```
    
2.  Start the Selenium Grid:
```bash
docker compose up -d
```

3.  Make request at [http://localhost:8000/browse](http://localhost:8000/browse)

```http
POST /browse
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `url` | `string` | **Required**. Url to print content |


    
4. Selenium Grid at [http://localhost:4444](http://localhost:4444).

⚙️ Configuration
----------------

Customize `docker-compose.yml` for specific needs. Disable OpenTelemetry by adding:

    environment:
      - JAVA_OPTS=-Dotel.traces.exporter=none

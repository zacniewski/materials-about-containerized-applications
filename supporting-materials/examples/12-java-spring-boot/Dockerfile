# Build stage
FROM maven:3.9-eclipse-temurin-21 AS build
WORKDIR /app

# Copy Maven project files
COPY pom.xml .
# Pre-fetch dependencies (layer caching)
RUN mvn -q -e -DskipTests dependency:go-offline || true

# Copy sources and build
COPY src ./src
RUN mvn -q -DskipTests package

# Runtime stage
FROM eclipse-temurin:21-jre
WORKDIR /app

# Create directory for H2 file-based DB
VOLUME ["/data"]

# Copy jar
COPY --from=build /app/target/todo-0.0.1-SNAPSHOT.jar app.jar

EXPOSE 8080

ENTRYPOINT ["java","-jar","/app/app.jar"]

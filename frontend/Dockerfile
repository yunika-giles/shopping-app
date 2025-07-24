# Use official Nginx image
FROM nginx:alpine

# Set environment variable for public HTML root
ENV NGINX_ROOT /usr/share/nginx/html

# Remove default Nginx index page
RUN rm -rf $NGINX_ROOT/*

# Copy your frontend files to the Nginx HTML directory
COPY index.html $NGINX_ROOT/

# Expose port 80
EXPOSE 80

# Start Nginx in foreground
CMD ["nginx", "-g", "daemon off;"]

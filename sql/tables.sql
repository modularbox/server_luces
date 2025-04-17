CREATE TABLE colors (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(50),
  red TINYINT UNSIGNED NOT NULL,
  green TINYINT UNSIGNED NOT NULL,
  blue TINYINT UNSIGNED NOT NULL
);

CREATE TABLE dmx_channels (
  id INT PRIMARY KEY AUTO_INCREMENT,
  channel_number INT NOT NULL UNIQUE,
  is_active BOOLEAN DEFAULT FALSE,
  use_custom_color BOOLEAN DEFAULT FALSE,
  color_id INT,
  red TINYINT UNSIGNED,
  green TINYINT UNSIGNED,
  blue TINYINT UNSIGNED,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (color_id) REFERENCES colors (id)
);

CREATE TABLE schedules (
  id INT PRIMARY KEY AUTO_INCREMENT,
  channel_id INT NOT NULL,
  day_of_week ENUM (
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
    'Sunday'
  ) NOT NULL,
  start_time TIME NOT NULL,
  end_time TIME NOT NULL,
  active BOOLEAN DEFAULT TRUE,
  FOREIGN KEY (channel_id) REFERENCES dmx_channels (id)
);

CREATE TABLE channel_status_log (
  id INT PRIMARY KEY AUTO_INCREMENT,
  channel_id INT,
  status BOOLEAN,
  color_id INT,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (channel_id) REFERENCES dmx_channels (id),
  FOREIGN KEY (color_id) REFERENCES colors (id)
);

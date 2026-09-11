import "./App.css";
import { useState } from "react";
import { motion } from "framer-motion";
import {
  Upload,
  Search,
  Settings,
  ChevronDown,
  ArrowUpRight,
  Activity,
  Moon,
  Sun,
  MapPin,
  X,
  Image as ImageIcon,
  CheckCircle,
  AlertCircle,
  LoaderCircle,
} from "lucide-react";

import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [activeTab, setActiveTab] = useState("Explore");
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });

  const [selectedImage, setSelectedImage] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);

  const [isEnhancing, setIsEnhancing] = useState(false);
  const [uploadResult, setUploadResult] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");

  const handleMouseMove = (event) => {
    const rect = event.currentTarget.getBoundingClientRect();

    const x = ((event.clientX - rect.left) / rect.width - 0.5) * 2;
    const y = ((event.clientY - rect.top) / rect.height - 0.5) * 2;

    setMousePosition({ x, y });
  };

  const handleMouseLeave = () => {
    setMousePosition({ x: 0, y: 0 });
  };

  const handleImageUpload = (event) => {
    const file = event.target.files?.[0];

    if (!file) return;

    setErrorMessage("");
    setUploadResult(null);

    const allowedTypes = [
      "image/jpeg",
      "image/jpg",
      "image/png",
      "image/tiff",
    ];

    if (!allowedTypes.includes(file.type)) {
      setErrorMessage(
        "Unsupported image format. Please use JPG, JPEG, PNG, or TIFF."
      );
      return;
    }

    if (file.size > 50 * 1024 * 1024) {
      setErrorMessage("Image size must be less than 50 MB.");
      return;
    }

    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
    }

    setSelectedImage(file);
    setPreviewUrl(URL.createObjectURL(file));
  };

  const clearImage = () => {
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
    }

    setSelectedImage(null);
    setPreviewUrl(null);
    setUploadResult(null);
    setErrorMessage("");
  };

  const handleEnhance = async () => {
    if (!selectedImage) {
      setErrorMessage("Please select an image first.");
      return;
    }

    setIsEnhancing(true);
    setErrorMessage("");
    setUploadResult(null);

    const formData = new FormData();
    formData.append("file", selectedImage);

    try {
      const response = await fetch(`${API_URL}/api/upload`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Image processing failed.");
      }

      setUploadResult(data);
    } catch (error) {
      setErrorMessage(
        error.message ||
          "Unable to connect to the backend. Please check whether FastAPI is running."
      );
    } finally {
      setIsEnhancing(false);
    }
  };

  return (
    <div className="app">
      <div className="stars" />
      <div className="atmosphere" />

      {/* Navigation */}
      <header className="navbar">
        <div className="brand">
          <div className="brand-icon">
            <Moon size={18} />
          </div>

          <div>
            <h1>LUNARIS</h1>
            <span>ORBITAL OBSERVATORY</span>
          </div>
        </div>

        <nav className="nav-links">
          {["Explore", "Missions", "Data"].map((item) => (
            <button
              key={item}
              className={activeTab === item ? "active" : ""}
              onClick={() => setActiveTab(item)}
            >
              {item}
            </button>
          ))}
        </nav>

        <div className="nav-actions">
          <button className="icon-button">
            <Search size={17} />
          </button>

          <button className="icon-button">
            <Settings size={17} />
          </button>

          <button className="profile-button">
            <div className="profile-avatar">AS</div>
            <span>Akshay</span>
            <ChevronDown size={15} />
          </button>
        </div>
      </header>

      {/* Main */}
      <main className="main-content">
        <section className="hero-section">
          <div className="hero-text">
            <div className="eyebrow">
              <span className="status-dot" />
              LIVE ORBITAL DATA
            </div>

            <h2>
              Explore the
              <br />
              <span>unknown.</span>
            </h2>

            <p>
              Navigate the lunar surface, inspect permanently shadowed
              regions, and uncover what lies beyond the light.
            </p>

            <button className="explore-button">
              <span>Explore the Moon</span>
              <ArrowUpRight size={17} />
            </button>
          </div>

          {/* Interactive Moon */}
          <div
            className="moon-stage"
            onMouseMove={handleMouseMove}
            onMouseLeave={handleMouseLeave}
          >
            <div
              className="cursor-light"
              style={{
                left: `${50 + mousePosition.x * 18}%`,
                top: `${50 + mousePosition.y * 18}%`,
              }}
            />

            <div className="orbit orbit-one" />
            <div className="orbit orbit-two" />

            <motion.div
              className="moon-wrapper"
              animate={{
                y: [0, -10, 0],
                rotate: [0, 1, 0, -1, 0],
                x: mousePosition.x * 8,
              }}
              transition={{
                y: {
                  duration: 8,
                  repeat: Infinity,
                  ease: "easeInOut",
                },
                rotate: {
                  duration: 8,
                  repeat: Infinity,
                  ease: "easeInOut",
                },
                x: {
                  duration: 0.6,
                  ease: "easeOut",
                },
              }}
            >
              <div
                className="moon"
                style={{
                  transform: `rotateX(${mousePosition.y * 4}deg) rotateY(${
                    mousePosition.x * 4
                  }deg)`,
                }}
              >
                <div
                  className="moon-glow"
                  style={{
                    transform: `translate(${mousePosition.x * 12}px, ${
                      mousePosition.y * 12
                    }px)`,
                  }}
                />

                <div className="moon-craters" />
                <div className="moon-shadow" />
              </div>
            </motion.div>

            {/* Floating markers */}
            <motion.div
              className="moon-marker marker-one"
              animate={{
                y: [0, -6, 0],
                x: mousePosition.x * 4,
              }}
              transition={{ duration: 4, repeat: Infinity }}
            >
              <MapPin size={13} />
              <span>PSR-01</span>
            </motion.div>

            <motion.div
              className="moon-marker marker-two"
              animate={{
                y: [0, 5, 0],
                x: mousePosition.x * 4,
              }}
              transition={{ duration: 5, repeat: Infinity }}
            >
              <MapPin size={13} />
              <span>CRATER 04</span>
            </motion.div>

            <motion.div
              className="moon-marker marker-three"
              animate={{
                y: [0, -4, 0],
                x: mousePosition.x * 4,
              }}
              transition={{ duration: 3.5, repeat: Infinity }}
            >
              <MapPin size={13} />
              <span>SHADOW ZONE</span>
            </motion.div>

            <div className="moon-caption">
              <span>01</span>
              <div />
              <span>MOON SURFACE</span>
            </div>
          </div>
        </section>

        {/* Information cards */}
        <section className="info-section">
          <div className="info-card">
            <div className="info-card-header">
              <div className="info-icon">
                <Activity size={17} />
              </div>

              <span>OBSERVATION STATUS</span>
            </div>

            <h3>Active mission</h3>
            <p>
              Monitoring permanently shadowed regions for low-light
              surface analysis.
            </p>

            <div className="info-progress">
              <div className="progress-bar">
                <div className="progress-fill" />
              </div>

              <span>72%</span>
            </div>
          </div>

          <div className="info-card">
            <div className="info-card-header">
              <div className="info-icon">
                <Sun size={17} />
              </div>

              <span>SURFACE CONDITIONS</span>
            </div>

            <h3>Low illumination</h3>
            <p>
              Ideal conditions for detecting subtle details in shadowed
              lunar terrain.
            </p>

            <div className="condition-row">
              <span>Illumination</span>
              <strong>0.04%</strong>
            </div>
          </div>

          {/* Upload card */}
          <div className="info-card upload-card">
            <div className="info-card-header">
              <div className="info-icon">
                <Upload size={17} />
              </div>

              <span>IMAGE ANALYSIS</span>
            </div>

            <h3>
              {isEnhancing
                ? "Processing image"
                : uploadResult
                ? "Image processed"
                : selectedImage
                ? "Image selected"
                : "Enhance your image"}
            </h3>

            <p>
              {isEnhancing
                ? "Uploading and validating your lunar image..."
                : uploadResult
                ? "Your image was successfully processed by the backend."
                : selectedImage
                ? "Your image is ready for processing."
                : "Upload a lunar image and reveal details hidden in the darkness."}
            </p>

            {selectedImage && previewUrl ? (
              <div className="selected-image">
                <img src={previewUrl} alt="Selected lunar image" />

                <div className="selected-image-info">
                  <div className="selected-image-name">
                    <ImageIcon size={14} />
                    <span>{selectedImage.name}</span>
                  </div>

                  <button
                    className="remove-image-button"
                    onClick={clearImage}
                    disabled={isEnhancing}
                  >
                    <X size={14} />
                  </button>
                </div>
              </div>
            ) : (
              <label className="upload-button">
                <Upload size={16} />
                Upload image

                <input
                  type="file"
                  accept="image/jpeg,image/jpg,image/png,image/tiff"
                  onChange={handleImageUpload}
                  hidden
                />
              </label>
            )}

            {selectedImage && !uploadResult && (
              <button
                className="enhance-button"
                onClick={handleEnhance}
                disabled={isEnhancing}
              >
                {isEnhancing ? (
                  <>
                    <LoaderCircle className="spin-icon" size={15} />
                    Processing...
                  </>
                ) : (
                  <>
                    <Activity size={15} />
                    Enhance image
                  </>
                )}
              </button>
            )}

            {uploadResult && (
              <div className="success-message">
                <CheckCircle size={16} />
                <span>Image uploaded and processed successfully.</span>
              </div>
            )}

            {errorMessage && (
              <div className="error-message">
                <AlertCircle size={16} />
                <span>{errorMessage}</span>
              </div>
            )}
          </div>
        </section>
      </main>

      <footer className="footer">
        <span>© 2026 LUNARIS OBSERVATORY</span>

        <div className="footer-right">
          <span>MISSION CONTROL</span>
          <span className="footer-status">
            <span className="status-dot" />
            SYSTEM OPERATIONAL
          </span>
        </div>
      </footer>
    </div>
  );
}

export default App;
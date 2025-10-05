import { useState } from 'react';
import axios from 'axios';

const ResumeForm = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    dob: '',
    state: '',
    gender: '',
    preferred_locations: [],
  });

  const [image, setImage] = useState(null);
  const [resumeFile, setResumeFile] = useState(null);

  const indianStates = ["Andhra Pradesh", "Bihar", "Delhi", "Karnataka", "Maharashtra", "Tamil Nadu"];
  const locations = ["Bangalore", "Mumbai", "Jaipur", "Delhi", "Chennai"];

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleCheckboxChange = (e) => {
    const value = e.target.value;
    setFormData(prev => {
      const current = [...prev.preferred_locations];
      if (current.includes(value)) {
        return { ...prev, preferred_locations: current.filter(loc => loc !== value) };
      } else {
        return { ...prev, preferred_locations: [...current, value] };
      }
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const payload = new FormData();
    payload.append('name', formData.name);
    payload.append('email', formData.email);
    payload.append('dob', formData.dob);
    payload.append('state', formData.state);
    payload.append('gender', formData.gender);
    payload.append('preferred_locations', formData.preferred_locations.join(','));
    payload.append('image', image);
    payload.append('resume_file', resumeFile);

    try {
      const res = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/resumes/upload`, payload, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      alert("Resume uploaded!");
      console.log(res.data);
    } catch (err) {
      console.error(err);
      alert("Upload failed");
    }
  };

  return (
    <div className="resume-form-container">
      <h2>Upload Resume App</h2>
      <form onSubmit={handleSubmit} className="resume-form">
        <label>Name:</label>
        <input name="name" type="text" value={formData.name} onChange={handleChange} required />

        <label>Email:</label>
        <input name="email" type="email" value={formData.email} onChange={handleChange} required />

        <label>Date of Birth:</label>
        <input name="dob" type="date" value={formData.dob} onChange={handleChange} required />

        <label>State:</label>
        <select name="state" value={formData.state} onChange={handleChange} required>
          <option value="">Select State</option>
          {indianStates.map(state => (
            <option key={state} value={state}>{state}</option>
          ))}
        </select>

        <label>Gender:</label>
        <div className="input-group">
          <label><input type="radio" name="gender" value="male" onChange={handleChange} required /> Male</label>
          <label><input type="radio" name="gender" value="female" onChange={handleChange} /> Female</label>
          <label><input type="radio" name="gender" value="other" onChange={handleChange} /> Other</label>
        </div>

        <label>Preferred Locations:</label>
        <div className="input-group">
          {locations.map(loc => (
            <label key={loc}>
              <input
                type="checkbox"
                value={loc}
                onChange={handleCheckboxChange}
              /> {loc}
            </label>
          ))}
        </div>

        <label>Upload Image:</label>
        <input type="file" accept="image/*" onChange={e => setImage(e.target.files[0])} required />

        <label>Upload Resume File:</label>
        <input type="file" accept=".pdf,.doc,.docx" onChange={e => setResumeFile(e.target.files[0])} required />

        <button type="submit">Submit</button>
      </form>
    </div>
  );
};

export default ResumeForm;

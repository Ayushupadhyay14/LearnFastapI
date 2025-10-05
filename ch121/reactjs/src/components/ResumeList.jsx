import { useEffect, useState } from 'react';
import axios from 'axios';

const ResumeList = () => {
  const [resumes, setResumes] = useState([]);
  useEffect(() => {
    const fetchResumes = async () => {
      try {
        const res = await axios.get('http://localhost:8000/resumes');
        setResumes(res.data);
      } catch (error) {
        console.error('Error fetching resumes:', error);
      }
    };
    fetchResumes();
  }, []);
  return (
    <div className="resume-list-container">
      <h2>Uploaded Resumes</h2>
      {resumes.length === 0 ? (
        <p>No resumes uploaded yet.</p>
      ) : (
        <table className="resume-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Email</th>
              <th>DOB</th>
              <th>State</th>
              <th>Gender</th>
              <th>Preferred Locations</th>
              <th>Image</th>
              <th>Resume</th>
            </tr>
          </thead>
          <tbody>
            {resumes.map((resume) => (
              <tr key={resume.id}>
                <td>{resume.id}</td>
                <td>{resume.name}</td>
                <td>{resume.email}</td>
                <td>{resume.dob}</td>
                <td>{resume.state}</td>
                <td>{resume.gender.charAt(0).toUpperCase() + resume.gender.slice(1)}</td>
                <td>{resume.preferred_locations}</td>
                <td>
                  <img src={`http://localhost:8000/${resume.image_path}`} width="60" />
                    
                </td>
                <td>
                  <a href={`http://localhost:8000/${resume.resume_file_path}`} target="_blank" rel="noopener noreferrer">
                    Download
                  </a>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}

export default ResumeList
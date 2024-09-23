import { createContext, useState } from "react";
import { getPeople, getProfiles } from "@/api/api";

export const DataContext = createContext();

export const DataProvider = ({ children }) => {
  const [loading, setLoading] = useState(false);
  const [userName, setUserName] = useState("Salai");
  const [profiles, setProfiles] = useState([]);
  const [people, setPeople] = useState([]);

  const fetchPeople = () => {
    setLoading(true);
    getPeople().then((response) => {
      setPeople(response.data);
      setLoading(false);
    });
  };

  const fetchProfiles = () => {
    getProfiles().then((response) => {
      setProfiles(response.data.profiles);
    });
  };

  return (
    <DataContext.Provider
      value={{
        loading,
        setLoading,
        userName,
        setUserName,
        people,
        setPeople,
        profiles,
        setProfiles,
        fetchPeople,
        fetchProfiles,
      }}
    >
      {children}
    </DataContext.Provider>
  );
};

import { createContext, useState } from "react";
import { getPeople, getProfiles } from "@/api/api";

export const DataContext = createContext();

export const DataProvider = ({ children }) => {
  const [loading, setLoading] = useState(false);
  const [userName, setUserName] = useState("Salai");
  const [profiles, setProfiles] = useState([]);
  const [people, setPeople] = useState([]);
  const [history, setHistory] = useState([]);

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

  const fetchHistory = () => {
    getHistory().then((response) => {
      setHistory(response.data);
    });
  }



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

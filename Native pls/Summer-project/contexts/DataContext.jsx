import { createContext, useState } from "react";
import { getPeople } from "@/api/api";

export const DataContext = createContext();

export const DataProvider = ({ children }) => {
  const [loading, setLoading] = useState(false);
  const [userName, setUserName] = useState("Salai");
  const [people, setPeople] = useState([]);

  const fetchPeople = () => {
    setLoading(true);
    getPeople().then((response) => {
      setPeople(response.data);
      setLoading(false);
    });
  };

  return (
    <DataContext.Provider
      value={{ loading, setLoading, userName, setUserName, people, setPeople, fetchPeople}}
    >
      {children}
    </DataContext.Provider>
  );
};
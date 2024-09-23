import BottomNavBar from "@/components/BottomBar";
import { useContext, useEffect } from "react";
import { DataContext } from "@/contexts/DataContext";

export default function Index() {
  const {fetchPeople, setLoading, fetchProfiles } = useContext(DataContext);

  useEffect(() => {
    setLoading(true);
    fetchPeople();
    fetchProfiles();
    setLoading(false);
  }, []);

  return <BottomNavBar />;
}

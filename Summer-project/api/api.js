import axios from "axios";

let user = "66d36a9d42d9a5784e1a59fe";
export const api = axios.create({
  baseURL: "http://10.16.49.101:5000",
  headers: {
    "Content-Type": "application/json",
  },
});

export const getPeople = async () => {
  const response = await api.get(`/people/${user}`);
  return response;
};

export const getNotifications = async () => {
  const response = await api.get(`/notifications/${user}`);
  return response;
};

export const getHistory = async () => {
  const response = await api.get(`/history/${user}`);
  return response;
};

export const getProfiles = async () => {
  const response = await api.get(`/profiles/${user}`);
  return response;
};

export const addPerson = async (formData) => {
  const response = await api.post("/people", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
  return response;
};

export const editProfile = async (profileId, formData) => {
  console.log("route: " + `/profiles/${user}/${profileId}`);
  const response = await api.put(
    `/profiles/${user}/${profileId}`,
    formData,
    {}
  );
  return response;
};

export const deletePerson = async (personId) => {
  const response = await api.delete(`/people/${user}/${personId}`);
  return response;
};

export const getActiveprofile = async () => {
  const response = await api.get(`/profiles/${user}/active`);
  return response;
};

export const getPermissions = async () => {
  const response = await api.get(`/permissions/${user}`);
  return response;
};

export const changePermission = async (permissionId, allow) => {
  const response = await api.put(`/permissions/${user}/${permissionId}`, {
    allow,
  });
  return response;
};

export const switchProfile = async (profileId) => {
  const response = await api.put(`/profiles/${user}/active`, {
    profile_id: profileId,
  });
  return response;
};
